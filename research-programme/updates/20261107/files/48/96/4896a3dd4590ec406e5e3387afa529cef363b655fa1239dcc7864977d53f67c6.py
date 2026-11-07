from hybrid_reference_common import *
import shutil


def main():
    modest()
    for model in ["heavy", "cold"]:
        equation = TemperatureEquation(model)
        for match in [20, 40]:
            folder = trace_path(model, match).parent
            if (folder / "COMPLETE").exists():
                assert verify_packet(folder)["accepted_reference_replay"]
                continue
            folder.mkdir(parents=True, exist_ok=False)
            owner = legacy_owner(model, match)
            source_path, old_path = owner / "physical-source.npz", owner / "physical-response.npz"
            saved = read_npz(old_path)
            old_attempt = ROOT / "results/legacy-replay" / f"{model}-m{match}"
            if (old_attempt / "COMPLETE").exists():
                original = verify_packet(old_attempt)
                result = read_npz(old_attempt / "trace.npz")
                retained = [row for row in original["checks"] if not row["passed"]]
                checks = [dict(row) for row in original["checks"] if row["name"].startswith("Replayed")]
                shutil.copyfile(old_attempt / "trace.npz", folder / "trace.npz")
                extra = [old_attempt / "status.json", old_attempt / "trace.npz"]
                diagnostics = None
            else:
                result, diagnostics = solve_response_trace(model, read_npz(source_path), 2048, equation.ladder,
                                                           equation.emission, equation.background, None)
                checks, retained, extra = [], [], []
                close(checks, "Replayed final physical feedback photons", result["photon"][-1], saved["photon_final"], 1e-10)
                for key in ["energy", "gas", "work"]:
                    close(checks, "Replayed physical feedback history:" + key, result[key], saved[key], 1e-10)
                for key, value in diagnostics.items():
                    limit = 1. if key == "energy_spectrum" else 1e-7
                    if value > limit:
                        retained.append(dict(name="Historical replay diagnostic:" + key, value=value, limit=limit, passed=False))
                np.savez_compressed(folder / "trace.npz", **result)
            matched = all(row["passed"] for row in checks)
            report = finish(folder, checks, [source_path, old_path, *equation.inputs, folder / "trace.npz", *extra],
                            accepted_reference_replay=matched, replay_scope="Reproduce the existing reference, not certify all inherited gas diagnostics",
                            retained_failed_checks=retained, inherited_diagnostics=diagnostics,
                            inherited_gas_error_repaired=False, new_source_evaluations=0, model=model, match=match)
            print(json.dumps(dict(case=f"{model}-m{match}", matched=matched, retained=retained)), flush=True)
            assert matched


if __name__ == "__main__":
    main()
