from hybrid_temperature_common import *


def main():
    modest()
    for model in ["heavy", "cold"]:
        equation = TemperatureEquation(model)
        for match in [20, 40]:
            folder = trace_path(model, match).parent
            if (folder / "COMPLETE").exists():
                assert verify_packet(folder)["all_checks_passed"]
                continue
            folder.mkdir(parents=True, exist_ok=False)
            owner = legacy_owner(model, match)
            source_path, old_path = owner / "physical-source.npz", owner / "physical-response.npz"
            source, saved = read_npz(source_path), read_npz(old_path)
            result, diagnostics = solve_response_trace(model, source, 2048, equation.ladder,
                                                       equation.emission, equation.background, None)
            checks = []
            close(checks, "Replayed final physical feedback photons", result["photon"][-1], saved["photon_final"], 1e-10)
            for key in ["energy", "gas", "work"]:
                close(checks, "Replayed physical feedback history:" + key, result[key], saved[key], 1e-10)
            for key, value in diagnostics.items():
                test(checks, "Feedback replay:" + key, value, 1e-7 if key != "energy_spectrum" else 1.)
            np.savez_compressed(folder / "trace.npz", **result)
            report = finish(folder, checks, [source_path, old_path, *equation.inputs, folder / "trace.npz"],
                            new_source_evaluations=0, replay_steps=2048, model=model, match=match)
            print(json.dumps(dict(case=f"{model}-m{match}", count=report["count"],
                                  failures=[row for row in checks if not row["passed"]])), flush=True)
            assert report["all_checks_passed"]


if __name__ == "__main__":
    main()
