from source_tangent import *


def main():
    modest()
    folder = ROOT / "results/state-precision-audit"
    folder.mkdir(parents=True, exist_ok=False)
    config = json.loads((ROOT / "configuration.json").read_text())
    bundle, theta = context(START)
    paired = PairedHistory(bundle, bundle)
    model = physics.FastSplit(paired, "difference")
    checks, records, inputs = [], [], [ROOT / "configuration.json", *bundle.inputs]
    import_precision = mp.mp.dps
    for record in config["selected"]:
        path = ROOT / "events/anchor" / f"event-{record['ordinal']:03d}.npz"
        with np.load(path) as saved:
            parameters, weight = physics.parameters_and_weight(theta, record["node"])
            results = []
            for precision in [60, 80]:
                with mp.workdps(precision):
                    value = -weight*model.state_correction(parameters)["total"]
                value = np.stack([value[..., :4], value[..., 4:]])
                value[:, LOW] = saved["high"][:, 3, LOW]
                results.append(value)
            denominator = np.maximum(photon_norm(saved["high"][:, 3], bundle.basis.mass), 1e-300)
            reconstruction = photon_norm(results[1]-saved["high"][:, 3], bundle.basis.mass)/denominator
            refinement = photon_norm(results[1]-results[0], bundle.basis.mass)/denominator
            for branch, history in np.ndindex(reconstruction.shape):
                label = f"{record['ordinal']}:{branch}:{history}"
                check(checks, "Saved-state high-mode precision:"+label, reconstruction[branch, history], 1e-10)
                check(checks, "60/80digit high-mode state agreement:"+label, refinement[branch, history], 1e-10)
            records.append(dict(event=record["ordinal"], saved_relative=reconstruction.tolist(),
                                precision_relative=refinement.tolist()))
            inputs.append(path)
    write_json(folder / "state-precision.json", records)
    inputs.append(folder / "state-precision.json")
    report = finish(folder, checks, inputs, fresh_import_mp_digits=import_precision,
                    source_changed=False, low_modes_excluded_because_independently_repaired=True)
    print(json.dumps(dict(count=report["count"], passed=report["all_checks_passed"],
                          import_digits=import_precision, maximum=max(max(max(row) for row in item["saved_relative"]) for item in records))), flush=True)


if __name__ == "__main__":
    main()
