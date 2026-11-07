from source_tangent import *


def main():
    modest()
    folder = ROOT / "results/stencil-impact"
    folder.mkdir(parents=True, exist_ok=False)
    verify(ROOT / "results/frozen")
    verify(ROOT / "results/prediction-test")
    saved = np.load(ROOT / "results/frozen/predictions.npz")
    actual = np.load(ROOT / "results/prediction-test/actuals.npz")
    mass = np.load(ROOT / "results/preparation/basis.npz")["mass"]
    checks, records = [], []
    delta = float(saved["delta"])
    for event in range(len(actual["high"])):
        derivatives = [(saved["derivative_high"][event, index], saved["derivative_low"][event, index])
                       for index in range(4)]
        tangent_change = precise_combine(derivatives[:2], [delta, -delta])
        curvature_change = precise_combine(derivatives[2:], [delta**2/2, -delta**2/2])
        second_change = precise_combine([tangent_change, curvature_change], [1, 1])
        denominator = np.maximum(photon_norm(actual["high"][event]+actual["low"][event], mass), 1e-300)
        first_relative = photon_norm(tangent_change[0]+tangent_change[1], mass)/denominator
        curvature_relative = photon_norm(curvature_change[0]+curvature_change[1], mass)/denominator
        second_relative = photon_norm(second_change[0]+second_change[1], mass)/denominator
        for branch, component, history in np.ndindex(second_relative.shape):
            records.append(dict(event=event, branch=branch, component=COMPONENTS[component], history=history,
                                first_prediction_step_change=float(first_relative[branch, component, history]),
                                curvature_contribution_step_change=float(curvature_relative[branch, component, history]),
                                second_prediction_step_change=float(second_relative[branch, component, history])))
        check(checks, f"Finite stencil-impact diagnostics:{event}",
              0 if np.isfinite(second_relative).all() else 1, .5)
    write_json(folder / "stencil-impact.json", records)
    inputs = [ROOT / "results/frozen/status.json", ROOT / "results/prediction-test/status.json",
              ROOT / "results/frozen/predictions.npz", ROOT / "results/prediction-test/actuals.npz",
              ROOT / "results/preparation/basis.npz", folder / "stencil-impact.json"]
    report = finish(folder, checks, inputs, diagnostic_only=True, original_derivative_gates_unchanged=True,
                    continuum_error_bound=False, predictions_changed=False)
    print(json.dumps(dict(checks=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
