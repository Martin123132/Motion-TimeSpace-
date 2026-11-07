from stage169_common import *
import argparse


def integrate(equation, initial, count, frozen_rates=False):
    state = equation.encode(initial)
    step = (equation.end - equation.begin) / count
    weights = np.array([.75, .25])
    tableau = np.array([[5/12, -1/12], [.75, .25]])
    nodes = np.array([1/3, 1.])
    identity = np.eye(97)
    maximum_residual = 0.
    history = [state.copy()]
    work = np.zeros(6)
    works = [work.copy()]
    anchor = equation.at(equation.begin)
    for index in range(count):
        left = equation.begin + index * step
        packets = [anchor if frozen_rates else equation.at(left + node * step) for node in nodes]
        matrix = np.block([[identity - step * tableau[0, 0] * packets[0][0],
                            -step * tableau[0, 1] * packets[1][0]],
                           [-step * tableau[1, 0] * packets[0][0],
                            identity - step * tableau[1, 1] * packets[1][0]]])
        right = np.vstack([state + step * sum(tableau[row, column] * packets[column][1] for column in range(2))
                           for row in range(2)])
        scale = np.maximum(np.max(abs(matrix), axis=1), 1e-300)
        stages = linalg.solve(matrix / scale[:, None], right / scale[:, None])
        residual = np.max(abs(matrix @ stages - right), axis=0)
        denominator = np.maximum(np.max(abs(matrix) @ abs(stages) + abs(right), axis=0), 1e-300)
        maximum_residual = max(maximum_residual, float(max(residual / denominator)))
        first, second = stages[:97], stages[97:]
        work += step * sum(weight * (value[96] - value[0]) for weight, value in zip(weights, [first, second]))
        state = second
        history.append(state.copy())
        works.append(work.copy())
        if index % 64 == 0:
            print(json.dumps(dict(model=equation.model, steps=count, completed=index + 1, frozen=frozen_rates)), flush=True)
    return np.array(history), np.array(works), maximum_residual


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=["heavy", "cold"])
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    folder = ROOT / "results" / ("smoke" if arguments.smoke else "frozen") / arguments.model
    folder.mkdir(parents=True, exist_ok=False)
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SEAL
    equation = TemperatureEquation(arguments.model)
    initial, paths = state_at(arguments.model, FRACTION_START, equation.basis)
    checks = []
    np.savez_compressed(folder / "initial.npz", **initial)
    outputs = {}
    for count in ([8, 16] if arguments.smoke else STEP_COUNTS):
        history, work, residual = integrate(equation, initial, count)
        output = equation.decode(history[-1])
        output.update(coordinate=np.linspace(equation.begin, equation.end, count + 1),
                      state=history, work=work)
        path = folder / f"prediction-{count}.npz"
        np.savez_compressed(path, **output)
        outputs[str(count)] = digest(path)
        test(checks, "Radau stage-equation backward error:" + str(count), residual, 1e-10)
        balance = history[:, 96] + work + (output["coordinate"] - equation.begin)[:, None] * equation.baseline
        scale = np.maximum(np.max(abs(history[:, 96]) + abs(work) + abs(output["coordinate"] - equation.begin)[:, None] * equation.baseline, axis=0), 1e-300)
        test(checks, "Radiation-gas-expansion work:" + str(count), float(max(np.max(abs(balance - balance[0]), axis=0) / scale)), 1e-7)
        close(checks, "Same baseline plus increment:" + str(count), history[..., 3:5], history[..., :1] + history[..., 1:3], 1e-8)
        checks.append(dict(name="Zero control:" + str(count), passed=bool(np.count_nonzero(history[..., -1]) == 0)))
    test(checks, "Inherited source-coordinate rewrite", equation.maximum_rewrite, 1e-10)
    if not arguments.smoke:
        history, work, residual = integrate(equation, initial, STEP_COUNTS[-1], True)
        path = folder / "constant-initial-control.npz"
        np.savez_compressed(path, **equation.decode(history[-1]), state=history, work=work)
        outputs["constant_control"] = digest(path)
        test(checks, "Constant control stage-equation backward error", residual, 1e-10)
    report = finish(folder, checks, [*paths, *equation.inputs, folder / "initial.npz", *folder.glob("*.npz")],
                    model=arguments.model, start=FRACTION_START, target=FRACTION_TARGET,
                    target_theta=equation.background.at(equation.end)["thermal_parameter"],
                    predictions_sha256=outputs, target_spectrum_used=False,
                    conditioning_source_curve="Stage166/168 current fixed cubic-labelled curve",
                    conditional_transport_prediction=True, microscopic_source_prediction=False,
                    source_raw_failures_retained=True)
    print(json.dumps(dict(model=arguments.model, count=report["count"],
                          failures=[row for row in checks if not row["passed"]])), flush=True)


if __name__ == "__main__":
    main()
