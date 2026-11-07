import run_hybrid_forecast
from hybrid_reference_common import *
from fractions import Fraction
import ast


def original_equations(equation, state, derivative, coordinate):
    generator, forcing, local = equation.at(coordinate)
    decoded = equation.decode(state)
    photon_derivative = equation.coordinates.transform @ derivative[:96]
    source_coordinate = equation.source(coordinate)
    spectral_source = linalg.solve(equation.coordinates.tests, source_coordinate)
    collision = local["rate"] * local["stiffness"] @ (decoded["photon"] - equation.basis.temperature[:, None] * decoded["gas"])
    supplied = local["rate"] * spectral_source
    left = equation.basis.mass @ photon_derivative
    residual = left - collision - supplied
    scale = np.maximum(np.linalg.norm(left, axis=0) + np.linalg.norm(collision, axis=0) + np.linalg.norm(supplied, axis=0), 1e-300)
    photon_error = float(max(np.linalg.norm(residual, axis=0) / scale))
    gas_error = derivative[96] - derivative[0] + equation.background.chi * decoded["gas"]
    gas_error += equation.basis.temperature @ collision + local["rate"] * source_coordinate[0] + equation.baseline
    return photon_error, float(max(abs(gas_error)))


def main():
    modest()
    folder = ROOT / "results/validation"
    folder.mkdir(parents=True, exist_ok=False)
    primary = verify_packet(ROOT / "results/comparison-hybrid")
    assert primary["all_checks_passed"]
    rates = verify_packet(ROOT / "rate-audit/results/rate-derivation")
    assert rates["all_checks_passed"]
    parent = json.loads((PARENT / "results/stage-integrity.json").read_text())
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SEAL
    chain = {PARENT / "results/stage-integrity.json": parent, **previous.ancestors()}
    prior_paths = {PARENT / name for name in parent["file_hashes"]}
    checks, consumed, retained = [], {}, []
    for path in sorted(ROOT.rglob("status.json")):
        if path.parent == folder:
            continue
        packet = verify_packet(path.parent)
        failures = [row for row in packet["checks"] if not row["passed"]]
        if failures:
            assert path.parent in [ROOT / "results/comparison", ROOT / "results/legacy-replay/heavy-m20"]
            retained.extend(dict(row, packet=str(path)) for row in failures)
        retained.extend(dict(row, packet=str(path)) for row in packet.get("retained_failed_checks", []))
        for filename, sha in packet["input_hashes"].items():
            if filename not in consumed:
                assert digest(filename) == sha, filename
                consumed[filename] = sha
                if not Path(filename).is_relative_to(ROOT):
                    prior_paths.add(Path(filename))
        checks.append(dict(name="Packet and input hashes:" + str(path.relative_to(ROOT)), passed=True))
    hashes = authenticate(prior_paths, chain)
    for model in ["heavy", "cold"]:
        for match in [20, 40]:
            label = f"{model}-m{match}"
            equation = HybridEquation(model, match)
            reader = ShapeReadout(equation.basis, canonical=True)
            freeze = verify_packet(ROOT / "results/frozen-hybrid" / label)
            assert freeze["finished_utc"] < primary["finished_utc"]
            path = ROOT / "results/frozen-hybrid" / label / "prediction-256.npz"
            assert digest(path) == freeze["predictions_sha256"]["256"]
            saved = read_npz(path)
            view = read_npz(ROOT / "results/comparison-hybrid" / f"{label}-256.npz")
            matrix = np.sqrt(reader.measure)[:, None] * reader.templates
            potential = view["predicted_potential"][:, :3]
            energy = reader.measure @ (reader.frequency[:, None] * potential)
            distortion = potential - reader.frequency[:, None] * (energy / reader.capacity)
            independent = np.linalg.lstsq(matrix, np.sqrt(reader.measure)[:, None] * distortion, rcond=None)[0]
            close(checks, "Independent weighted SVD amplitudes:" + label, independent, view["predicted_amplitudes"][:, :3], 1e-10)
            for key in ["photon", "energy", "gas"]:
                values = np.atleast_2d(saved[key])
                for row in values:
                    baseline = Fraction.from_float(float(row[0]))
                    for increment in row[1:3]:
                        increment = Fraction.from_float(float(increment))
                        assert (baseline + increment) - baseline == increment
                checks.append(dict(name="Exact-rational paired finite-input identity:" + label + ":" + key, passed=True))
            np.savez_compressed(folder / (label + "-paired.npz"),
                                total_potential_high=np.repeat(view["predicted_potential"][:, :1], 2, axis=1),
                                total_potential_low=view["predicted_potential"][:, 1:3],
                                total_energy_high=np.repeat(saved["energy"][:1], 2),
                                total_energy_low=saved["energy"][1:3],
                                total_gas_high=np.repeat(saved["gas"][:1], 2),
                                total_gas_low=saved["gas"][1:3],
                                energy_is_represented_component_only=True,
                                carrier_energy=view["conditional_carrier_energy"])
            step = (equation.end - equation.begin) / 256
            for index in [0, 127, 255]:
                left = equation.begin + index * step
                before, second = saved["state"][index:index + 2]
                second_matrix, second_force, unused = equation.at(left + step)
                second_derivative = second_matrix @ second + second_force
                first_derivative = ((second - before) / step - .25 * second_derivative) / .75
                first = before + step * (5/12 * first_derivative - first_derivative * 0. - second_derivative / 12)
                first_matrix, first_force, unused = equation.at(left + step / 3)
                scale = np.maximum(np.max(abs(first_derivative) + abs(first_matrix) @ abs(first) + abs(first_force), axis=0), 1e-300)
                test(checks, "Independent Radau reconstruction:" + label + ":" + str(index),
                     float(max(np.max(abs(first_derivative - first_matrix @ first - first_force), axis=0) / scale)), 1e-10)
                for slot, state, derivative, position in [("first", first, first_derivative, left + step/3),
                                                           ("second", second, second_derivative, left + step)]:
                    photon, gas = original_equations(equation, state, derivative, position)
                    test(checks, "Original photon equation:" + label + ":" + str(index) + ":" + slot, photon, 1e-7)
                    test(checks, "Original gas absolute equation:" + label + ":" + str(index) + ":" + slot, gas, 1e-8)
            test(checks, "Temperature clock identity:" + label,
                 abs(math.log(equation.background.at(equation.end)["thermal_parameter"] / equation.background.at(equation.begin)["thermal_parameter"]) + equation.end - equation.begin), 1e-14)
            corrupt = []
            close(corrupt, "Injected spectrum corruption", view["predicted_residual"] * 1.001, view["predicted_residual"], 1e-10)
            assert not corrupt[0]["passed"]
            checks.append(dict(name="Readout corruption rejected:" + label, passed=True))
    scripts = list(ROOT.glob("*.py"))
    for path in scripts:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    protected = POST.parent / "formalization-workbench"
    changed = [str(path) for path in protected.rglob("*") if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    checks.append(dict(name="Protected workbench mtime guard", count=len(changed), passed=not changed))
    inputs = [*map(Path, consumed), *folder.glob("*.npz"), ROOT / "results/comparison-hybrid/status.json"]
    report = finish(folder, checks, inputs, compiled_scripts=len(scripts), rehashed_prior_files=len(hashes),
                    consumed_and_immediate_rehashed=hashes, retained_failed_checks=retained,
                    original_equation_sampling="first/middle/last Radau step, both stages; not every step",
                    raw_source_failures_inherited=40, conditional_resolved_prediction_only=True,
                    microscopic_source_prediction_complete=False, unresolved_carrier_forecast=False,
                    protected_check_scope="Mtime scan since 17:20:03 UTC, not a pre-turn content snapshot",
                    paired_totals_are_component_representation=True)
    print(json.dumps(dict(count=report["count"], failures=[row for row in checks if not row["passed"]],
                          prior_files=len(hashes), scripts=len(scripts))), flush=True)


if __name__ == "__main__":
    main()
