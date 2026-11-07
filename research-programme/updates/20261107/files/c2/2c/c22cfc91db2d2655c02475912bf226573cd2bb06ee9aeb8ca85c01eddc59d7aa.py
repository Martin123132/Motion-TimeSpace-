from source_tangent import *


def main():
    modest()
    mp.mp.dps = 60
    folder = ROOT / "results/state-overlays"
    folder.mkdir(parents=True, exist_ok=False)
    assert not (ROOT / "events/target").exists()
    config = json.loads((ROOT / "configuration.json").read_text())
    anchor, unused = context(START)
    checks, records, inputs = [], [], [ROOT / "configuration.json", ROOT / "PRECISION-REPAIR.md"]
    for tag, offset in OFFSETS.items():
        verify(ROOT / "events" / tag)
        inputs.append(ROOT / "events" / tag / "status.json")
        bundle, theta = context(START-offset/config["expansion_span"])
        paired = PairedHistory(bundle, anchor)
        model = physics.FastSplit(paired, "difference")
        inputs.extend(paired.inputs)
        nodes = {order: {node["index"]: node for node in physics.integration_nodes(theta, order)}
                 for order in [6, 7, 8]}
        output = folder / tag
        output.mkdir()
        for record in config["selected"]:
            original = ROOT / "events" / tag / f"event-{record['ordinal']:03d}.npz"
            with np.load(original) as saved:
                high, low = saved["high"].copy(), saved["low"].copy()
                parameters, weight = physics.parameters_and_weight(theta, nodes[record["order"]][record["node"]["index"]])
                assert weight == float(saved["weight"])
                evaluated = []
                for precision in [60, 80]:
                    with mp.workdps(precision):
                        state = -weight*model.state_correction(parameters)["total"]
                    state = np.stack([state[..., :4], state[..., 4:]])
                    state[:, LOW] = high[:, 3, LOW]
                    evaluated.append(state)
                scale = np.maximum(photon_norm(evaluated[1], bundle.basis.mass), 1e-300)
                uncertainty = photon_norm(evaluated[1]-evaluated[0], bundle.basis.mass)/scale
                change = photon_norm(evaluated[1]-high[:, 3], bundle.basis.mass)/scale
                for branch, history in np.ndindex(uncertainty.shape):
                    check(checks, f"60/80 state agreement:{tag}:{record['ordinal']}:{branch}:{history}",
                          uncertainty[branch, history], 1e-10)
                high[:, 3] = evaluated[1]
                for component, indices in [(4, [1, 2, 3]), (5, [0, 1, 2, 3])]:
                    high[:, component], low[:, component] = precise_combine(
                        [(high[:, index], low[:, index]) for index in indices], [1]*len(indices))
                assert np.array_equal(high[:, :3], saved["high"][:, :3])
                assert np.array_equal(high[:, 3, LOW], saved["high"][:, 3, LOW])
                destination = output / original.name
                np.savez_compressed(destination, high=high, low=low, original_path=str(original),
                                    original_sha256=digest(original), state_precision=80)
                inputs.extend([original, destination])
                records.append(dict(phase=tag, event=record["ordinal"], change=change.tolist(),
                                    refinement=uncertainty.tolist()))
    write_json(folder / "state-repair-records.json", records)
    inputs.append(folder / "state-repair-records.json")
    report = finish(folder, checks, inputs, target_source_evaluated=False,
                    original_bank_changed=False, temperature_curve_changed=False,
                    tolerances_changed=False, overlay_events=60)
    print(json.dumps(dict(count=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
