import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import run_hybrid_forecast
from hybrid_reference_common import *
import mpmath as mp
import argparse
from test_temperature_forecast import weighted_norm


def precise(values):
    return mp.matrix(np.atleast_2d(values).tolist())


def maximum(values):
    return max(abs(value) for value in values)


def refine(matrix, right):
    floating = np.array(matrix.tolist(), dtype=float)
    scale = np.maximum(np.max(abs(floating), axis=1), 1e-300)
    factor = linalg.lu_factor(floating / scale[:, None])
    answer = precise(linalg.lu_solve(factor, np.array(right.tolist(), dtype=float) / scale[:, None]))
    diagnostic = []
    for unused in range(8):
        residual = right - matrix * answer
        error = maximum(residual) / max(maximum(right), mp.mpf("1e-300"))
        diagnostic.append(float(error))
        if error < mp.mpf("1e-45"):
            break
        correction = linalg.lu_solve(factor, np.array(residual.tolist(), dtype=float) / scale[:, None])
        answer += precise(correction)
    assert diagnostic[-1] < 1e-30, diagnostic
    return answer, diagnostic


def operator(equation, coordinate):
    local = equation.background.at(float(coordinate))
    theta = local["thermal_parameter"]
    rate = mp.mpf(float(local["coefficient"] / theta))
    stiffness = precise(equation.ladder.at(theta, 0)[:96, :96] - equation.emission.at(theta, "dcbr"))
    temperature = precise(equation.basis.temperature).T
    collision = rate * stiffness
    coupled = collision * temperature
    energy_row = temperature.T * collision
    matrix = mp.zeros(97)
    matrix[:96, :96] = collision
    matrix[:96, 96] = -coupled
    matrix[96, :96] = -energy_row
    matrix[96, 96] = (temperature.T * coupled)[0] - mp.mpf(equation.background.chi)
    source = precise(equation.source(float(coordinate))[:, :3])
    spectral = mp.zeros(96, 3)
    for index, frequency in enumerate(equation.coordinates.others):
        spectral[int(frequency), :] = source[index + 1, :]
    spectral[equation.coordinates.pivot, :] = (source[0, :] - temperature.T * spectral) / temperature[equation.coordinates.pivot]
    forcing = mp.zeros(97, 3)
    forcing[:96, :] = rate * spectral
    forcing[96, :] = -rate * source[0, :]
    forcing[96, 0] -= 1
    return matrix, forcing


def main():
    modest()
    mp.mp.dps = 80
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    folder = ROOT / "results" / ("original-step-smoke" if args.smoke else "original-step-audit")
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, diagnostics = [], [], {}
    for model in (["heavy"] if args.smoke else ["heavy", "cold"]):
        for match in ([20] if args.smoke else [20, 40]):
            label = f"{model}-m{match}"
            equation = HybridEquation(model, match)
            reader = ShapeReadout(equation.basis, canonical=True)
            origin = ROOT / "results/frozen-hybrid" / label
            path = origin / "prediction-256.npz"
            saved = read_npz(path)
            mass = mp.zeros(97)
            mass[:96, :96] = precise(equation.basis.mass)
            heat = mp.mpf(equation.background.chi)
            mass[96, 96] = heat
            energy = precise(equation.basis.energy)
            temperature = precise(equation.basis.temperature)
            energy_row = temperature * mass[:96, :96]
            step = mp.mpf((equation.end - equation.begin) / 256)
            tableau = [[mp.mpf(5)/12, -mp.mpf(1)/12], [mp.mpf(3)/4, mp.mpf(1)/4]]
            for index in ([0] if args.smoke else [0, 127, 255]):
                left = equation.begin + index * float(step)
                current = precise(saved["state"][index, :, :3])
                initial = mp.zeros(97, 3)
                for slot, frequency in enumerate(equation.coordinates.others):
                    initial[int(frequency), :] = current[slot + 1, :]
                pivot = equation.coordinates.pivot
                initial[pivot, :] = (current[0, :] - energy * initial[:96, :]) / energy[0, pivot]
                initial[96, :] = (current[96, :] - current[0, :]) / heat
                packets = [operator(equation, left + float(step)/3), operator(equation, left + float(step))]
                matrix, right = mp.zeros(194), mp.zeros(194, 3)
                for row in range(2):
                    right[row*97:(row+1)*97, :] = mass * initial
                    for column in range(2):
                        matrix[row*97:(row+1)*97, column*97:(column+1)*97] = -step * tableau[row][column] * packets[column][0]
                        if row == column:
                            matrix[row*97:(row+1)*97, column*97:(column+1)*97] += mass
                        right[row*97:(row+1)*97, :] += step * tableau[row][column] * packets[column][1]
                stages, convergence = refine(matrix, right)
                first, second = stages[:97, :], stages[97:, :]
                derivatives = [(mp.mpf(3)/2*(first-initial) + (second-initial)/2)/step,
                               (-mp.mpf(9)/2*(first-initial) + mp.mpf(5)/2*(second-initial))/step]
                for slot, state in enumerate([first, second]):
                    left_side = mass * derivatives[slot]
                    collision = packets[slot][0] * state
                    residual = left_side - collision - packets[slot][1]
                    relative = max(maximum(residual[:96, column]) / max(maximum(left_side[:96, column]) + maximum(collision[:96, column]) + maximum(packets[slot][1][:96, column]), mp.mpf("1e-300")) for column in range(3))
                    test(checks, f"80-digit original photon equation:{label}:{index}:{slot}", float(relative), 1e-7)
                    test(checks, f"80-digit original gas absolute equation:{label}:{index}:{slot}", float(maximum(residual[96, :])), 1e-8)
                supplied = step * mp.matrix([[1, 0, 0]])
                balance = energy_row*(second[:96, :]-initial[:96, :]) + heat*(second[96, :]-initial[96, :])
                balance += step*heat*(mp.mpf(3)/4*first[96, :] + second[96, :]/4) + supplied
                denominator = max(maximum(energy_row*initial[:96, :]) + maximum(heat*initial[96, :]) + maximum(supplied), mp.mpf("1e-300"))
                test(checks, f"80-digit original energy/work:{label}:{index}", float(maximum(balance)/denominator), 1e-7)
                predicted = np.array(second.tolist(), dtype=float)
                target = equation.decode(saved["state"][index + 1])
                relative_photon = weighted_norm(reader.values @ (predicted[:96] - target["photon"][:, :3]), reader.measure) / np.maximum(weighted_norm(reader.values @ target["photon"][:, :3], reader.measure), 1e-300)
                relative_gas = abs(predicted[96] - target["gas"][:3]) / np.maximum(abs(target["gas"][:3]), 1e-300)
                for column, name in enumerate(COLUMNS[:3]):
                    test(checks, f"Unchanged-step photon agreement:{label}:{index}:{name}", relative_photon[column], .01)
                    test(checks, f"Unchanged-step gas agreement:{label}:{index}:{name}", relative_gas[column], .01)
                detail = dict(refinement_residuals=convergence, state=[[mp.nstr(value, 80) for value in row] for row in second.tolist()],
                              photon_difference=relative_photon.tolist(), gas_difference=relative_gas.tolist())
                diagnostics[f"{label}:{index}"] = detail
                print(json.dumps(dict(case=label, index=index, photon=relative_photon.tolist(), gas=relative_gas.tolist(), iterations=len(convergence))), flush=True)
            inputs.extend([*equation.inputs, path, origin / "status.json"])
    write_json(folder / "precise-states.json", diagnostics)
    report = finish(folder, checks, [*inputs, folder / "precise-states.json"], sampled_steps=[0] if args.smoke else [0, 127, 255],
                    arithmetic_digits=80, independently_solved_original_variables=True,
                    saved_forecast_changed=False, sampled_one_step_check_only=True,
                    old_failed_derivative_reconstruction_not_relabelled=True)
    print(json.dumps(dict(count=report["count"], failures=[row for row in checks if not row["passed"]])), flush=True)


if __name__ == "__main__":
    main()
