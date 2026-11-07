from source_tangent import *


def main():
    modest()
    folder = ROOT / "results/prediction-test"
    folder.mkdir(parents=True, exist_ok=False)
    frozen = verify(ROOT / "results/frozen")
    target = verify(ROOT / "events/target")
    assert frozen["all_predictions_written"] and not frozen["target_source_evaluated"]
    assert target["target_source_evaluated"] and target["event_count"] == frozen["event_count"]
    frozen_time = datetime.fromisoformat(frozen["finished_utc"])
    config = json.loads((ROOT / "configuration.json").read_text())
    basis = np.load(ROOT / "results/preparation/basis.npz")
    prediction = np.load(ROOT / "results/frozen/predictions.npz")
    mass = basis["mass"]
    checks, records, moment_records = [], [], []
    inputs = [ROOT / "results/frozen/status.json", ROOT / "events/target/status.json",
              ROOT / "results/preparation/basis.npz", ROOT / "results/frozen/predictions.npz"]
    actuals, actual_lows = [], []
    for record in config["selected"]:
        ordinal = record["ordinal"]
        path = ROOT / "events/target" / f"event-{ordinal:03d}.npz"
        inputs.append(path)
        with np.load(path) as saved:
            assert datetime.fromisoformat(str(saved["finished_utc"])) > frozen_time
            actual = (saved["high"], saved["low"])
            actuals.append(actual[0])
            actual_lows.append(actual[1])
            target_norm = photon_norm(actual[0]+actual[1], mass)
            for order_index, order in enumerate([1, 2]):
                proposed = (prediction["high"][ordinal, order_index], prediction["low"][ordinal, order_index])
                difference = precise_combine([proposed, actual], [1, -1])
                relative = photon_norm(difference[0]+difference[1], mass)/np.maximum(target_norm, 1e-300)
                for branch, component, history in np.ndindex(relative.shape):
                    name = f"order{order}:{ordinal}:{branch}:{COMPONENTS[component]}:{history}"
                    check(checks, name, relative[branch, component, history], .01)
                    records.append(dict(order=order, event=ordinal, panel=record["panel"],
                                        branch=["moving_history", "fixed_incident"][branch],
                                        component=COMPONENTS[component], history=history,
                                        relative=float(relative[branch, component, history]),
                                        actual_norm=float(target_norm[branch, component, history])))
                    with mp.workdps(80):
                        errors = {}
                        for label, row in [("energy", 0), ("number", 1), ("gas", 97)]:
                            index = (branch, component, row, history)
                            denominator = abs(mp.mpf(float(actual[0][index]))+mp.mpf(float(actual[1][index])))
                            numerator = abs(mp.mpf(float(difference[0][index]))+mp.mpf(float(difference[1][index])))
                            errors[label] = float(numerator/max(denominator, mp.mpf("1e-300")))
                    moment_records.append(dict(order=order, event=ordinal, branch=branch,
                                               component=COMPONENTS[component], history=history, **errors))
    write_json(folder / "photon-prediction-checks.json", records)
    write_json(folder / "moment-prediction-diagnostics.json", moment_records)
    np.savez_compressed(folder / "actuals.npz", high=np.array(actuals), low=np.array(actual_lows))
    inputs += [folder / "photon-prediction-checks.json", folder / "moment-prediction-diagnostics.json",
               folder / "actuals.npz"]
    summary = {}
    for order in [1, 2]:
        for branch in ["moving_history", "fixed_incident"]:
            for component in COMPONENTS:
                values = [row["relative"] for row in records if
                          row["order"] == order and row["branch"] == branch and row["component"] == component]
                summary[f"order{order}/{branch}/{component}"] = dict(count=len(values),
                    passed=sum(value < .01 for value in values), maximum=max(values), median=float(np.median(values)))
    report = finish(folder, checks, inputs, summary=summary, tolerance=.01,
                    source_adopted=False, source_curve_changed=False, full_population_integral=False,
                    frozen_before_all_target_events=True, native_incident_histories_are_inputs=True)
    print(json.dumps(dict(checks=report["count"], failed=sum(not row["passed"] for row in checks),
                          summary=summary)), flush=True)


if __name__ == "__main__":
    main()
