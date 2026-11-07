from source_tangent import *


def main():
    modest()
    folder = ROOT / "results/error-decomposition"
    folder.mkdir(parents=True, exist_ok=False)
    verify(ROOT / "results/frozen")
    verify(ROOT / "results/prediction-test")
    saved = np.load(ROOT / "results/frozen/predictions.npz")
    actual = np.load(ROOT / "results/prediction-test/actuals.npz")
    mass = np.load(ROOT / "results/preparation/basis.npz")["mass"]
    factor = la.cholesky(mass, lower=True)
    checks, records = [], []
    for event in range(len(actual["high"])):
        for order_index in range(2):
            proposed = (saved["high"][event, order_index], saved["low"][event, order_index])
            measured = (actual["high"][event], actual["low"][event])
            error = precise_combine([proposed, measured], [1, -1])
            kernel = (error[0][1], error[1][1])
            history = precise_combine([(error[0][0], error[1][0]), kernel], [1, -1])
            reconstructed = precise_combine([kernel, history], [1, 1])
            difference = precise_combine([reconstructed, (error[0][0], error[1][0])], [1, -1])
            relative = photon_norm(difference[0]+difference[1], mass)/np.maximum(
                photon_norm(error[0][0]+error[1][0], mass), 1e-300)
            check(checks, f"Exact kernel/history decomposition:{event}:{order_index+1}", np.max(relative), 1e-10)
            for component in range(6):
                target = la.solve_triangular(factor, (measured[0]+measured[1])[0, component, 1:97], lower=True)
                kernel_vector = la.solve_triangular(factor, (kernel[0]+kernel[1])[component, 1:97], lower=True)
                history_vector = la.solve_triangular(factor, (history[0]+history[1])[component, 1:97], lower=True)
                denominator = np.maximum(np.sum(target**2, axis=0), 1e-300)
                kernel_square = np.sum(kernel_vector**2, axis=0)/denominator
                history_square = np.sum(history_vector**2, axis=0)/denominator
                cross = 2*np.sum(kernel_vector*history_vector, axis=0)/denominator
                total_square = np.sum((kernel_vector+history_vector)**2, axis=0)/denominator
                for column in range(4):
                    records.append(dict(event=event, order=order_index+1, component=COMPONENTS[component],
                        history=column, kernel_relative=float(np.sqrt(kernel_square[column])),
                        incident_history_relative=float(np.sqrt(history_square[column])),
                        cross_relative_square=float(cross[column]), total_relative=float(np.sqrt(total_square[column]))))
                error_square = np.max(abs(total_square-kernel_square-history_square-cross))/max(
                    float(np.max(total_square)), float(np.max(kernel_square+history_square)), 1e-300)
                check(checks, f"Squared norm cross term:{event}:{order_index+1}:{component}", error_square, 1e-10)
    write_json(folder / "decomposition.json", records)
    inputs = [ROOT / "results/frozen/status.json", ROOT / "results/prediction-test/status.json",
              ROOT / "results/frozen/predictions.npz", ROOT / "results/prediction-test/actuals.npz",
              ROOT / "results/preparation/basis.npz", ROOT / "HISTORY-REGULARITY.md",
              folder / "decomposition.json"]
    report = finish(folder, checks, inputs, predictions_changed=False, source_curve_changed=False,
                    diagnostic_only=True, moving_history_differences_are_finite_step_not_smoothness_proof=True)
    print(json.dumps(dict(checks=report["count"], passed=report["all_checks_passed"])), flush=True)


if __name__ == "__main__":
    main()
