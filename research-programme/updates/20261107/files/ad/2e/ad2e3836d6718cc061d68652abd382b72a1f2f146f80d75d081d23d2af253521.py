from common import *
from adjoint_operator import *
from compact_adjoint import CompactAdjoint
import time

def main():
    modest()
    check_parent()
    require(read(ROOT / "evolution-validation.json")["passed"], "new independent evolution qualified")
    write(ROOT / "frozen-inputs.json", dict(sources={str(path): digest(path) for path in STAGE.iterdir() if path.suffix in (".py", ".md", ".ps1")},
          branches=BRANCHES, algebra=ALGEBRA, numerical=GATE, coefficient_grid="original nodes only",
          terminal_targets=["D", "delta_c"], output_normalization="GR interval envelope, no target discrepancy"))
    (ROOT / "contexts").mkdir(exist_ok=False)
    (ROOT / "coefficients").mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        system = open_owned(model, "contexts")
        grid = system.background["efold"]
        size = len(system.core)
        directory = ROOT / "coefficients" / model
        directory.mkdir(exist_ok=False)
        print(model, "core", size, "dimension", len(system.units), "nodes", len(grid), flush=True)
        started = time.monotonic()
        parts, receipts = [], []
        structural = np.zeros((size, size), dtype=bool)
        for start in range(0, len(grid), 128):
            stop = min(start + 128, len(grid))
            values = {name: [] for name in ("base", "injection", "channels", "rows", "speeds")}
            for index in range(start, stop):
                if index % 32 == 0:
                    guard()
                extracted = extract(system, float(grid[index]))
                for name, value in zip(values, extracted):
                    values[name].append(value)
            packet = {name: np.array(value) for name, value in values.items()}
            packet["efold"] = grid[start:stop]
            path = directory / ("chunk-" + str(start).zfill(5) + ".npz")
            np.savez_compressed(path, **packet)
            receipts.append(dict(path=str(path), sha256=digest(path), start=start, stop=stop))
            structural |= np.any(packet["base"] != 0., axis=0)
            parts.append({name: value for name, value in packet.items() if name != "base"})
            print(model, "saved", stop, "/", len(grid), "seconds", round(time.monotonic() - started, 1), flush=True)
        packet = {name: np.concatenate([part[name] for part in parts]) for name in parts[0]}
        base_rows, base_columns = np.nonzero(structural)
        packet["base"] = np.empty((len(grid), len(base_rows)))
        for receipt in receipts:
            guard()
            chunk = load(receipt["path"])
            packed = chunk["base"][:, base_rows, base_columns]
            restored = np.zeros_like(chunk["base"])
            restored[:, base_rows, base_columns] = packed
            require(np.array_equal(restored, chunk["base"]), "lossless every-node coefficient packing")
            packet["base"][receipt["start"]:receipt["stop"]] = packed
            del chunk, packed, restored
        packet["base_rows"], packet["base_columns"] = base_rows, base_columns
        quadrupoles = np.array([int(np.flatnonzero(system.core == system.context["all_moments"][2, node])[0]) for node in range(5)])
        packet.update(core_size=np.array(size), units=system.units, wave=np.array(system.wave), quadrupoles=quadrupoles)
        require(np.array_equal(system.units[size:].reshape(190, 5), np.tile(system.units[size:size + 5], (190, 1))), "constant hierarchy units")
        path = directory / "operator.npz"
        np.savez_compressed(path, **packet)
        operator = CompactAdjoint(packet)
        indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
        points = grid[indices] + .43 * (grid[indices + 1] - grid[indices])
        errors = {}
        identities = {}
        for index, efold in enumerate(points):
            guard()
            vector = np.sin(np.arange(len(system.units)) + index + 1.)
            dual = np.cos(np.arange(len(system.units)) + index + .7)
            groups = dict(alpha=[system.alpha_slot], cdm=[system.cdm_slot], core=np.arange(size), tail=np.arange(size, len(vector)))
            if model == "heavy":
                groups["heavy"] = system.slots
            for branch, label in enumerate(BRANCHES):
                expected = system.evaluate(float(efold), vector * system.units, label)
                expected_gr = system.evaluate(float(efold), vector * system.units, "gr")
                actual = operator.apply(float(efold), vector, branch)
                target = expected[0] / system.units
                for name, selection in groups.items():
                    key = label + "_" + name
                    value = relative(actual[selection] - target[selection], target[selection])
                    errors[key] = max(errors.get(key, 0.), value)
                transposed = operator.apply(float(efold), dual, branch, transpose=True)
                identities[label + "_transpose"] = max(identities.get(label + "_transpose", 0.), abs(np.dot(dual, actual) - np.dot(transposed, vector)) / max(np.linalg.norm(dual) * np.linalg.norm(actual), 1e-80))
                core, _, _, _, injection, channel = operator.blocks(float(efold), branch)
                direct_channels = np.array([expected[1]["Psi"] - expected_gr[1]["Psi"], expected[3]["z"] - expected_gr[3]["z"]])
                source = injection @ direct_channels
                direct_difference = (expected[0] - expected_gr[0]) / system.units
                errors[label + "_rank_two"] = max(errors.get(label + "_rank_two", 0.), relative(source - direct_difference[:size], direct_difference[:size]))
                errors[label + "_channel_rows"] = max(errors.get(label + "_channel_rows", 0.), relative(channel @ vector[:size] - direct_channels, direct_channels))
                identities[label + "_tail_difference"] = max(identities.get(label + "_tail_difference", 0.), sup(direct_difference[size:]))
            row_actual = operator.splines["rows"](float(efold)) @ vector[:size]
            row_expected = np.array([expected_gr[1]["D"], expected_gr[1]["delta_c"]])
            for row, name in enumerate(("D", "delta_c")):
                errors["readout_" + name] = max(errors.get("readout_" + name, 0.), abs(row_actual[row] - row_expected[row]) / max(abs(row_expected[row]), 1e-80))
        passed = all(value < GATE and np.isfinite(value) for value in errors.values()) and all(value < ALGEBRA and np.isfinite(value) for value in identities.values())
        report = dict(model=model, passed=bool(passed), core_size=size, dimension=len(system.units), nodes=len(grid),
                      packet=str(path), sha256=digest(path), chunks=receipts, numerical=errors, algebra=identities,
                      seconds=time.monotonic() - started, packing=dict(core_entries=size**2, retained_entries=len(base_rows), exact_zero_only=True, every_node_roundtrip=True))
        write(ROOT / (model + "-build.json"), report)
        print(model, "qualification", report["numerical"], report["algebra"], "passed", passed, flush=True)
        reports.append(report)
        require(passed, "inspect coefficient/transpose failure before proceeding")
        del operator, packet, parts, system
    check_parent()
    write(ROOT / "build-result.json", dict(passed=True, reports=reports))
    print("coupled adjoint coefficients qualified", flush=True)

if __name__ == "__main__":
    main()
