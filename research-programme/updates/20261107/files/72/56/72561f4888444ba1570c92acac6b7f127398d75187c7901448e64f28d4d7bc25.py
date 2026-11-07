from source_tangent import *
from freeze_predictions import read_pair


def main():
    modest()
    folder = ROOT / "results/frozen"
    assert not (ROOT / "events/target").exists() and not (folder / "COMPLETE").exists()
    folder.mkdir(parents=True, exist_ok=True)
    overlays = verify(ROOT / "results/state-overlays")
    assert overlays["all_checks_passed"] and overlays["overlay_events"] == 60
    config = json.loads((ROOT / "configuration.json").read_text())
    mass = np.load(ROOT / "results/preparation/basis.npz")["mass"]
    inputs = [ROOT / "configuration.json", ROOT / "results/preparation/basis.npz",
              ROOT / "results/state-overlays/status.json", ROOT / "PRECISION-REPAIR.md",
              ROOT / "HISTORY-REGULARITY.md", ROOT / "SECOND-DERIVATIVE.md"]
    checks, records, predictions, lows, derivatives, derivative_lows = [], [], [], [], [], []
    delta = config["delta_log_temperature"]
    for record in config["selected"]:
        ordinal = record["ordinal"]
        pairs = {}
        for tag in OFFSETS:
            path = ROOT / "results/state-overlays" / tag / f"event-{ordinal:03d}.npz"
            pairs[tag] = read_pair(path)
            inputs.append(path)
        tangents, curvatures = [], []
        for step, plus, minus in [(.01, "plus", "minus"), (.005, "plus_half", "minus_half")]:
            tangents.append(precise_combine([pairs[plus], pairs[minus]], [1/(2*step), -1/(2*step)]))
            curvatures.append(precise_combine([pairs[plus], pairs["anchor"], pairs[minus]],
                                             [1/step**2, -2/step**2, 1/step**2]))
        first = precise_combine([pairs["anchor"], tangents[1]], [1, delta])
        second = precise_combine([first, curvatures[1]], [1, delta**2/2])
        predictions.append(np.stack([first[0], second[0]]))
        lows.append(np.stack([first[1], second[1]]))
        derivatives.append(np.stack([tangents[0][0], tangents[1][0], curvatures[0][0], curvatures[1][0]]))
        derivative_lows.append(np.stack([tangents[0][1], tangents[1][1], curvatures[0][1], curvatures[1][1]]))
        for name, values in [("tangent", tangents), ("curvature", curvatures)]:
            difference = precise_combine(values, [1, -1])
            relative = photon_norm(difference[0]+difference[1], mass)/np.maximum(
                photon_norm(values[1][0]+values[1][1], mass), 1e-300)
            for branch, component, history in np.ndindex(relative.shape):
                check(checks, f"{ordinal}:{branch}:{COMPONENTS[component]}:{history}:{name}",
                      relative[branch, component, history], .01)
                records.append(dict(event=ordinal, branch=branch, component=COMPONENTS[component],
                                    history=history, derivative=name,
                                    relative=float(relative[branch, component, history])))
    path = folder / "predictions.npz"
    np.savez_compressed(path, high=np.array(predictions), low=np.array(lows),
                        derivative_high=np.array(derivatives), derivative_low=np.array(derivative_lows),
                        delta=delta, target_theta=config["theta0"]*math.exp(delta), orders=np.array([1, 2]),
                        histories=np.array(["heavy-join1", "heavy-join2", "cold-join1", "cold-join2"]))
    inputs.append(path)
    write_json(folder / "derivative-checks.json", records)
    inputs.append(folder / "derivative-checks.json")
    finish(folder, checks, inputs, all_predictions_written=True, target_source_evaluated=False,
           target_source_read=False, event_count=len(config["selected"]), prediction_orders=[1, 2],
           source_curve_used=False, full_population_integral=False, state_precision_repaired_before_freeze=True,
           original_event_bank_changed=False, moving_history_is_finite_step_variation=True,
           native_incident_histories_are_inputs=True,
           differentiation_failures=sum(not row["passed"] for row in checks))
    print(json.dumps(dict(frozen=True, checks=len(checks), failed=sum(not row["passed"] for row in checks),
                          prediction_sha256=digest(path))), flush=True)


if __name__ == "__main__":
    main()
