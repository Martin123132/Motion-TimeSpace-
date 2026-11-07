import csv
from common import ROOT, HIERARCHY, WAVE, GATE, ALGEBRA, modest, guard, require, read, write, digest, load
import numpy as np
from scipy.interpolate import CubicSpline

OUTPUT = ROOT / "comparison-corrected"


def errors(prediction, target):
    return np.max(abs(prediction - target), axis=0) / np.maximum(np.max(abs(target), axis=0), 1e-30)


def physical(packet):
    names = packet["observer_names"].tolist()
    get = lambda name: packet["observer"][:, names.index(name)]
    scale, hubble = get("a_native"), get("H_native")
    enthalpy = get("R") + get("Pbar")
    alpha = get("sigma") / WAVE
    phi = get("eta_sync") - hubble * alpha
    return dict(Phi=phi, Psi=2 * get("Weyl") - phi, D=get("D_sync") - 3 * hubble * enthalpy * alpha,
                Q=get("Q_sync") + enthalpy * get("sigma"), Pi=get("Pi"), theta_c=WAVE * get("sigma"),
                delta_c=get("delta_cdm64") - 3 * hubble * alpha, delta_b=get("delta_baryon64") - 3 * hubble * alpha,
                delta_gamma=get("delta_gamma64") - 4 * hubble * alpha, delta_massless=get("delta_massless64") - 4 * hubble * alpha,
                a=scale, H=hubble, R=enthalpy, Phi_rate=get("Weyl_prime") + get("Pi_prime") / (2 * WAVE ** 2))


def constraints(values):
    expressions = dict(Hamiltonian=[2 * WAVE ** 2 * values["Phi"], values["D"], 3 * values["H"] * values["Q"] / WAVE],
                       slip=[values["Phi"], -values["Psi"], -values["Pi"] / WAVE ** 2],
                       momentum=[values["Phi_rate"], values["H"] * values["Psi"], -values["Q"] / (2 * WAVE)])
    result = {}
    for name, terms in expressions.items():
        array = np.array(terms)
        result[name] = float(np.max(abs(array.sum(axis=0))) / max(float(np.max(abs(array))), 1e-30))
    return result


def newton_budget(packet, probe_indices):
    values = physical(packet)
    times, scale = packet["times"], values["a"]
    poisson = -values["D"] / (2 * WAVE ** 2)
    momentum = -3 * values["H"] * values["Q"] / (2 * WAVE ** 3)
    shear = -values["Pi"] / WAVE ** 2
    force_scale = max(float(np.max(abs(values["Psi"]))), 1e-30)
    velocity_scale = max(float(np.max(abs(values["theta_c"]))), 1e-30)
    split = float(np.max(abs(values["Psi"] - poisson - momentum - shear)) / force_scale)
    replays = []
    for stride in (1, 2, 4):
        keep = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
        antiderivative = CubicSpline(times[keep], scale[keep] * values["Psi"][keep]).antiderivative()
        replays.append((scale[0] * values["theta_c"][0] + WAVE ** 2 * (antiderivative(times[probe_indices]) - antiderivative(times[0]))) / scale[probe_indices])
    poisson_integral = CubicSpline(times, scale * poisson).antiderivative()
    poisson_velocity = (scale[0] * values["theta_c"][0] + WAVE ** 2 * (poisson_integral(times[probe_indices]) - poisson_integral(times[0]))) / scale[probe_indices]
    correction = CubicSpline(times, scale * (values["Psi"] - poisson))
    widths = np.diff(times)
    cell_budget = sum(abs(correction.c[index]) * widths ** (4 - index) / (4 - index) for index in range(4))
    accumulated = WAVE ** 2 * np.r_[0., np.cumsum(cell_budget)] / scale
    signed_change = replays[0] - poisson_velocity
    replay_error = float(np.max(abs(replays[0] - values["theta_c"][probe_indices])) / velocity_scale)
    source_refinement = max(float(np.max(abs(candidate - replays[0])) / velocity_scale) for candidate in replays[1:])
    bound_excess = float(np.max(np.maximum(abs(signed_change) - accumulated[probe_indices], 0)) / velocity_scale)
    report = dict(split_error=split, velocity_replay_error=replay_error, source_refinement=source_refinement, force_poisson_difference=float(np.max(abs(values["Psi"] - poisson)) / force_scale),
                  force_triangle_budget=float((np.max(abs(momentum)) + np.max(abs(shear))) / force_scale),
                  velocity_poisson_difference=float(np.max(abs(signed_change)) / velocity_scale), velocity_interpolant_budget=float(np.max(accumulated[probe_indices]) / velocity_scale),
                  bound_excess=bound_excess, passed=bool(max(split, bound_excess) < ALGEBRA and max(replay_error, source_refinement) < GATE),
                  scope="force approximation on corrected relativistic sources; not independently evolved Poisson cosmology or static local PPN")
    arrays = dict(times=times[probe_indices], a=scale[probe_indices], theta=values["theta_c"][probe_indices], theta_replayed=replays[0], theta_poisson=poisson_velocity, absolute_velocity_bound=accumulated[probe_indices],
                  force_times=times, Psi=values["Psi"], Psi_poisson=poisson, momentum_correction=momentum, shear_correction=shear)
    return report, arrays


def main():
    modest()
    OUTPUT.mkdir(exist_ok=False)
    owner = read(ROOT / "prediction-result.json")
    require(owner["state"] == "complete" and len(owner["reports"]) == 2, "completed mutually coupled calculation")
    require(owner["source_sha256"] == digest(ROOT / "run_coupled_extension.py"), "prediction owner")
    reports, rows = [], []
    for model_owner in owner["reports"]:
        guard()
        model = model_owner["model"]
        original = load(HIERARCHY / "runs-balanced" / model / "native-reference.npz")
        packets = {}
        for case in model_owner["cases"]:
            path = ROOT / "runs" / model / case["file"]
            require(digest(path) == case["sha256"], "case owner")
            packets[case["tag"]] = load(path)
            require(np.array_equal(packets[case["tag"]]["times"], original["times"]), "original phase grid")
        values = {tag: physical(packet) for tag, packet in packets.items()}
        inherited = physical(dict(observer=original["observer"], observer_names=original["observer_names"]))
        signal_names = [name for name in inherited if name not in ("a", "H", "R")]
        replay_state = float(np.max(errors(packets["L16-base"]["projected_state"], original["state"])))
        replay_physical = {name: float(errors(values["L16-base"][name], inherited[name])) for name in signal_names}
        pairs = [("L64 precision", "L64-base", "L64-fine"), ("L128 precision", "L128-base", "L128-fine"),
                 ("64/128 angular", "L64-fine", "L128-fine"), ("128/G192 angular", "L128-fine", "G192-fine")]
        comparisons = []
        for label, left, right in pairs:
            state_error = float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))
            source_errors = {name: float(errors(values[left][name], values[right][name])) for name in signal_names}
            comparisons.append(dict(label=label, left=left, right=right, state_error=state_error, physical_errors=source_errors, passed=bool(max(state_error, *source_errors.values()) < GATE)))
        algebra = {tag: constraints(value) for tag, value in values.items()}
        zero_state = bool(np.count_nonzero(packets["L64-zero"]["projected_state"]) == 0 and np.count_nonzero(packets["L64-zero"]["tail_norms"]) == 0)
        zero_sources = all(np.count_nonzero(values["L64-zero"][name]) == 0 for name in signal_names)
        negative = float(np.max(errors(-packets["L64-negative"]["projected_state"], packets["L64-base"]["projected_state"])))
        negative_sources = {name: float(errors(-values["L64-negative"][name], values["L64-base"][name])) for name in signal_names}
        changed = {name: float(errors(inherited[name], values["G192-fine"][name])) for name in signal_names}
        changed64 = {name: float(errors(values["L16-base"][name], values["L64-fine"][name])) for name in signal_names}
        newton = {}
        for tag in ("L16-base", "L64-fine", "L128-fine", "G192-fine"):
            budget, arrays = newton_budget(packets[tag], original["probes"])
            output = ROOT / (model + "-" + tag + "-newton.npz")
            saved_budget = load(output)
            require(set(saved_budget) == set(arrays) and all(np.array_equal(saved_budget[name], value) for name, value in arrays.items()), "original budget arrays must remain identical")
            budget.update(file=output.name, sha256=digest(output))
            newton[tag] = budget
        low = packets["G192-fine"]["low_slots"]
        quadrupole_change = errors(original["state"][:, low], packets["G192-fine"]["projected_state"][:, low])
        scalar_subset = original["selected"]
        selected_change = errors(original["state"][:, scalar_subset], packets["G192-fine"]["projected_state"][:, scalar_subset])
        passed = bool(max(replay_state, *replay_physical.values(), negative, *negative_sources.values()) < GATE and all(row["passed"] for row in comparisons) and max(value for row in algebra.values() for value in row.values()) < ALGEBRA and zero_state and zero_sources and all(row["passed"] for row in newton.values()))
        report = dict(model=model, passed=passed, finite16_state_replay=replay_state, finite16_physical_replay=replay_physical, comparisons=comparisons, algebra=algebra,
                      zero_state=zero_state, zero_sources=zero_sources, negative_state_error=negative, negative_source_errors=negative_sources, physical_change_from_original=changed, physical_change_16_to64=changed64,
                      massive_quadrupole_change=quadrupole_change.tolist(), selected_state_change=selected_change.tolist(), selected_native_indices=original["mapping"][scalar_subset].tolist(),
                      newton=newton, no_future_species_histories_supplied=True, original_action_retained=True, old_closure_failure_preserved=True)
        reports.append(report)
        for name in signal_names:
            rows.append(dict(model=model, observable=name, old_to_corrected_change=changed[name], old16_replay=replay_physical[name],
                             precision64=comparisons[0]["physical_errors"][name], precision128=comparisons[1]["physical_errors"][name], angular64_128=comparisons[2]["physical_errors"][name], angular128_G192=comparisons[3]["physical_errors"][name]))
        print(dict(model=model, passed=passed, replay=replay_state, comparisons=[(row["label"], row["state_error"], max(row["physical_errors"].values())) for row in comparisons], changes=changed, quadrupoles=quadrupole_change.tolist(), newton=newton["G192-fine"]), flush=True)
    with (ROOT / "physical-comparison.csv").open(newline="", encoding="utf-8") as stream:
        original_rows = list(csv.DictReader(stream))
    require(original_rows == [{key: str(value) for key, value in row.items()} for row in rows], "existing CSV changed")
    result = dict(passed=all(row["passed"] for row in reports), reports=reports, source_sha256=digest(__file__), prediction_result_sha256=digest(ROOT / "prediction-result.json"), csv_sha256=digest(ROOT / "physical-comparison.csv"), numerical_gate=GATE, algebra_gate=ALGEBRA, force_budget_scope="same corrected relativistic source; no self-consistent Poisson-system substitution")
    write(OUTPUT / "comparison-result.json", result)
    require(result["passed"], "coupled comparison failed; preserve all outputs and inspect")


if __name__ == "__main__":
    main()

