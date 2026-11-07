from source_tangent import *


def main():
    modest()
    folder = ROOT / "results/batch-validation"
    folder.mkdir(parents=True, exist_ok=False)
    config = json.loads((ROOT / "configuration.json").read_text())
    verify(ROOT / "events/plus_half")
    bundle, theta = context(START-OFFSETS["plus_half"]/config["expansion_span"])
    fixed, unused = context(START)
    record = config["selected"][0]
    nodes = {node["index"]: node for node in physics.integration_nodes(theta, record["order"])}
    parameters, weight = physics.parameters_and_weight(theta, nodes[record["node"]["index"]])
    scalar, loop_path, reused = virtual(parameters)
    path = ROOT / "events/plus_half/event-000.npz"
    saved = np.load(path)
    checks, inputs = [], [path, loop_path, ROOT / "configuration.json",
                         ROOT / "events/plus_half/status.json", *bundle.inputs, *fixed.inputs]
    for branch, incident in enumerate([bundle, fixed]):
        high, low, diagnostics = evaluate(parameters, incident, models(incident), scalar)
        high, low = precise_combine([(high, low)], [-weight])
        difference = precise_combine([(high, low), (saved["high"][branch], saved["low"][branch])], [1, -1])
        norms = photon_norm(difference[0]+difference[1], bundle.basis.mass)/np.maximum(
            photon_norm(high+low, bundle.basis.mass), 1e-300)
        for component, history in np.ndindex(norms.shape):
            check(checks, f"Independent unbatched source:{branch}:{COMPONENTS[component]}:{history}",
                  norms[component, history], 1e-10)
        for name, value in diagnostics.items():
            check(checks, f"Unbatched identity:{branch}:{name}", value, 1e-10)
        np.savez_compressed(folder / f"branch-{branch}.npz", high=high, low=low)
        inputs.append(folder / f"branch-{branch}.npz")
    report = finish(folder, checks, inputs, target_predictions_changed=False,
                    source_curve_changed=False, compared_at_nonzero_temperature_offset=True)
    print(json.dumps(dict(checks=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
