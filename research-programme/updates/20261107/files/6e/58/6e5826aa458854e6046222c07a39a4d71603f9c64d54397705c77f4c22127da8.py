from source_tangent import *


def main():
    modest()
    frozen = verify(ROOT / "results/frozen")
    folder = ROOT / "results/tangent-interpretation"
    folder.mkdir(parents=True, exist_ok=False)
    basis = np.load(ROOT / "results/preparation/basis.npz")
    factor = la.cholesky(basis["mass"], lower=True)
    saved = np.load(ROOT / "results/frozen/predictions.npz")
    checks, records, inputs = [], [], [ROOT / "results/frozen/status.json",
                                      ROOT / "results/frozen/predictions.npz",
                                      ROOT / "results/preparation/basis.npz"]
    for event in range(frozen["event_count"]):
        path = ROOT / "events/anchor" / f"event-{event:03d}.npz"
        inputs.append(path)
        with np.load(path) as anchor:
            source = anchor["high"]+anchor["low"]
        tangent = saved["derivative_high"][event, 1]+saved["derivative_low"][event, 1]
        for branch, component in np.ndindex(source.shape[:2]):
            initial = la.solve_triangular(factor, source[branch, component, 1:97], lower=True)
            derivative = la.solve_triangular(factor, tangent[branch, component, 1:97], lower=True)
            history = la.solve_triangular(factor, tangent[0, component, 1:97]-tangent[1, component, 1:97], lower=True)
            denominator = np.maximum(np.sum(initial**2, axis=0), 1e-300)
            exponent = np.sum(initial*derivative, axis=0)/denominator
            turning = np.linalg.norm(derivative-initial*exponent, axis=0)/np.sqrt(denominator)
            history_rate = np.linalg.norm(history, axis=0)/np.sqrt(denominator)
            for column in range(4):
                records.append(dict(event=event, branch=branch, component=COMPONENTS[component],
                    history=column, local_parallel_log_slope=float(exponent[column]),
                    local_shape_turning_rate=float(turning[column]),
                    incident_history_tangent_rate=float(history_rate[column])))
            reconstructed = initial*exponent+(derivative-initial*exponent)
            error = np.linalg.norm(derivative-reconstructed)/max(np.linalg.norm(derivative), 1e-300)
            check(checks, f"Orthogonal tangent reconstruction:{event}:{branch}:{component}", error, 1e-10)
    write_json(folder / "tangent-components.json", records)
    inputs.append(folder / "tangent-components.json")
    report = finish(folder, checks, inputs, source_curve_changed=False, predictions_changed=False,
                    interpretation_only=True, exponent_fitted_as_new_model=False)
    print(json.dumps(dict(count=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
