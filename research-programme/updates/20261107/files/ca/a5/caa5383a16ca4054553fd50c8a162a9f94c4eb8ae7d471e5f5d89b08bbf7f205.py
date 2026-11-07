from hybrid_temperature_common import *
from freeze_temperature_forecast import integrate
import argparse


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=["heavy", "cold"])
    arguments = parser.parse_args()
    for match in [20, 40]:
        label = f"{arguments.model}-m{match}"
        folder = ROOT / "results/frozen-hybrid" / label
        folder.mkdir(parents=True, exist_ok=False)
        equation = HybridEquation(arguments.model, match)
        initial, inputs = corrected_state_at(arguments.model, FRACTION_START, equation.basis, match)
        np.savez_compressed(folder / "initial.npz", **initial)
        checks, outputs = [], {}
        for count in STEP_COUNTS:
            states, work, residual = integrate(equation, initial, count)
            prediction = equation.decode(states[-1])
            path = folder / f"prediction-{count}.npz"
            np.savez_compressed(path, **prediction, state=states, work=work,
                                coordinate=np.linspace(equation.begin, equation.end, count + 1))
            outputs[str(count)] = digest(path)
            test(checks, "Radau backward equation error:" + str(count), residual, 1e-10)
            balance = states[:, 96] + work + np.linspace(0, equation.end - equation.begin, count + 1)[:, None] * equation.baseline
            scale = np.maximum(np.max(abs(states[:, 96]) + abs(work) + np.linspace(0, equation.end - equation.begin, count + 1)[:, None] * equation.baseline, axis=0), 1e-300)
            test(checks, "Radiation/gas/work:" + str(count), float(max(np.max(abs(balance - balance[0]), axis=0) / scale)), 1e-7)
            checks.append(dict(name="Zero solution:" + str(count), passed=bool(np.count_nonzero(states[..., -1]) == 0)))
        states, work, residual = integrate(equation, initial, STEP_COUNTS[-1], True)
        path = folder / "constant-initial-control.npz"
        np.savez_compressed(path, **equation.decode(states[-1]), state=states, work=work)
        outputs["constant_control"] = digest(path)
        test(checks, "Constant control backward equation error", residual, 1e-10)
        test(checks, "Source rewrite", equation.maximum_rewrite, 1e-10)
        report = finish(folder, checks, [*inputs, *equation.inputs, *folder.glob("*.npz"), ROOT / "REPAIR-NOTES.md"],
                        model=arguments.model, match=match, start=FRACTION_START, target=FRACTION_TARGET,
                        target_theta=equation.background.at(equation.end)["thermal_parameter"],
                        predictions_sha256=outputs, target_resolved_spectrum_used=False,
                        unresolved_carrier_is_conditioning_input=True, post_mapping_repair_not_blinded=True,
                        source_curve_changed=False, tolerances_changed=False)
        print(json.dumps(dict(case=label, count=report["count"], failures=[row for row in checks if not row["passed"]])), flush=True)
        assert report["all_checks_passed"]


if __name__ == "__main__":
    main()
