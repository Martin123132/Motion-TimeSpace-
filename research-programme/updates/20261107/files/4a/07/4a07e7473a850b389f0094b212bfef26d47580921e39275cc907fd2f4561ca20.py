import csv
import time
from common import ROOT, PRIOR, GATE, ALGEBRA, modest, guard, check_prior, require, read, write, digest, load
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicHermiteSpline, PchipInterpolator
from numpy.polynomial.legendre import leggauss

WAVE = 5.0


def relative(left, right):
    return float(np.max(abs(left - right)) / max(float(np.max(abs(right))), 1e-80))


def symbolic_checks():
    ell = sp.symbols("ell", integer=True, positive=True)
    plain = lambda index: 2 * index + 1
    polar = lambda index: (2 * index + 1) * (index + 2) * (index + 1) / (index * (index - 1))
    upper = (ell + 3) * (ell - 1) / ((ell + 1) * (2 * ell + 1))
    pol_terminal = (ell + 1) * (ell + 2) * (ell - 2) / (ell * (ell - 1))
    identities = [
        plain(ell) * (ell + 1) / (2 * ell + 1) - plain(ell + 1) * (ell + 1) / (2 * ell + 3),
        polar(ell) * upper - polar(ell + 1) * (ell + 1) / (2 * ell + 3),
        plain(ell - 1) * ell / (2 * ell - 1) - ell,
        polar(ell - 1) * (ell + 2) * (ell - 2) / (ell * (2 * ell - 1)) - pol_terminal * ell / (ell - 2),
    ]
    simplified = [str(sp.simplify(value)) for value in identities]
    require(simplified == ["0"] * 4, "streaming weight derivation")
    collision = sp.Matrix([[-sp.Rational(9, 10), sp.Rational(3, 5)], [sp.Rational(1, 10), -sp.Rational(2, 5)]])
    metric = sp.diag(5, 30)
    require(metric * collision == collision.T * metric, "quadrupole collision symmetry")
    rates = sorted(-value for value in collision.eigenvals())
    require(rates == [sp.Rational(3, 10), sp.Integer(1)], "quadrupole dissipation")
    return dict(streaming_identities=simplified, quadrupole_collision_rates=[str(value) for value in rates])


def groups_for(reference):
    signature = reference["signature"]
    state_map = reference["mapping"]
    def position(native_index):
        return int(np.flatnonzero(state_map == native_index)[0])
    groups = []
    specifications = [("photon", int(signature[3]), int(signature[6]), False, False),
                      ("polarization", int(signature[5]), int(signature[7]), True, False)]
    for eigen in range(int(signature[20])):
        maximum = int(signature[40 + eigen])
        start = int(signature[50 + eigen])
        for momentum in range(int(signature[30 + eigen])):
            specifications.append((f"neutrino-{eigen}-{momentum}", start + momentum * (maximum + 1), maximum, False, True))
    for name, base, maximum, polarized, massive in specifications:
        require(maximum > 3, "tail length")
        moments = np.arange(3, maximum + 1)
        indices = np.array([position(base + int(ell)) for ell in moments])
        low = position(base + 2)
        weights = (2 * moments + 1).astype(float)
        if polarized:
            weights *= (moments + 2) * (moments + 1) / (moments * (moments - 1))
            weights[-1] = (maximum + 1) * (maximum + 2) * (maximum - 2) / (maximum * (maximum - 1))
        else:
            weights[-1] = maximum
        streaming = np.zeros((len(moments), len(moments)))
        for row, ell in enumerate(moments):
            if row > 0:
                streaming[row, row - 1] = WAVE * ell / (2 * ell + 1) if ell < maximum else WAVE * (maximum / (maximum - 2) if polarized else 1)
            if row + 1 < len(moments):
                streaming[row, row + 1] = -WAVE * ((ell + 3) * (ell - 1) / (ell + 1) if polarized else ell + 1) / (2 * ell + 1)
        symmetry = weights[:, None] * streaming + streaming.T * weights[None, :]
        require(np.max(abs(symmetry)) < ALGEBRA, "derived streaming antisymmetry")
        groups.append(dict(name=name, indices=indices, low=low, weights=weights, streaming=streaming,
                           massive=massive, polarized=polarized, maximum=maximum, input_coefficient=3 * WAVE / 7,
                           output_coefficient=-WAVE / 3 if polarized else -3 * WAVE / 5,
                           terminal_coefficient=maximum + (3 if polarized else 1)))
    all_indices = np.concatenate([group["indices"] for group in groups])
    require(len(np.unique(all_indices)) == len(all_indices), "overlapping tails")
    return groups, all_indices


def norm_bound(times, opacity, speed, drive, drive_rate, initial, weight, stride=1, order=16):
    keep = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
    source = CubicHermiteSpline(times[keep], drive[keep], drive_rate[keep])
    damping = PchipInterpolator(times[keep], opacity[keep])
    antiderivative = damping.antiderivative()
    velocity = PchipInterpolator(times[keep], speed[keep])
    nodes, quadrature = leggauss(order)
    half = np.diff(times) / 2
    middle = (times[1:] + times[:-1]) / 2
    points = middle[:, None] + half[:, None] * nodes
    attenuation = np.exp(-(antiderivative(times[1:])[:, None] - antiderivative(points)))
    forcing = np.sqrt(weight) * 3 * WAVE / 7 * velocity(points) * abs(source(points))
    increments = half * np.sum(quadrature * attenuation * forcing, axis=1)
    transfer = np.exp(-np.diff(antiderivative(times)))
    result = np.empty(len(times))
    result[0] = initial
    for index in range(len(transfer)):
        result[index + 1] = transfer[index] * result[index] + increments[index]
    return result


def main():
    modest()
    check_prior()
    source_result = read(ROOT / "input-result.json")
    require(source_result["passed"] and source_result["source_sha256"] == digest(ROOT / "prepare_tail_inputs.py"), "input owner")
    symbolic = symbolic_checks()
    destination = ROOT / "results"
    destination.mkdir(exist_ok=False)
    reports, all_rows = [], []
    for source_record in source_result["reports"]:
        guard()
        model = source_record["model"]
        folder = PRIOR / "runs-balanced" / model
        reference, audit = load(folder / "native-reference.npz"), load(folder / "operator-audit.npz")
        require(digest(source_record["file"]) == source_record["sha256"], "thermal input ownership")
        background = load(source_record["file"])
        times = reference["times"]
        time_indices = background["reference_indices"]
        opacity = background["opacity"][time_indices]
        scale_factor = background["scale_factor"][time_indices]
        groups, tail_indices = groups_for(reference)
        core_indices = np.array([index for index in range(len(reference["mapping"])) if index not in tail_indices])
        require(len(tail_indices) == 154 and len(core_indices) == (30 if model == "heavy" else 28), "retained partition")
        require(reference["signature"][12] == 1, "massless UFA remains in core")
        model_root = destination / model
        model_root.mkdir()
        group_reports, kernel_reports = [], []
        lower, upper = times[0], times[-1]
        opacity_curve = PchipInterpolator(background["times"], background["opacity"])
        optical = opacity_curve.antiderivative()
        scale_curve = PchipInterpolator(background["times"], background["scale_factor"])
        full, fine = load(folder / "full.npz"), load(folder / "precision.npz")
        for group in groups:
            indices, low, weights = group["indices"], group["low"], group["weights"]
            initial_speed = float(audit["matrices"][0, indices[0], low] / group["input_coefficient"])
            require(0 < initial_speed <= 1 + ALGEBRA, "physical streaming speed")
            mass_ratio = max(initial_speed ** -2 - 1, 0.) if group["massive"] else 0.
            group["mass_ratio"] = mass_ratio
            group["initial_scale_factor"] = scale_factor[0]
            speed = 1 / np.sqrt(1 + mass_ratio * (scale_factor / scale_factor[0]) ** 2)
            damping = np.zeros_like(times) if group["massive"] else opacity
            rate = reference["derivative"][:, indices]
            tail = reference["state"][:, indices]
            driving = reference["state"][:, low]
            expected_rate = speed[:, None] * (tail @ group["streaming"].T) - damping[:, None] * tail
            expected_rate[:, 0] += group["input_coefficient"] * speed * driving
            expected_rate[:, -1] -= group["terminal_coefficient"] / times * tail[:, -1]
            energy = .5 * np.sum(weights * tail ** 2, axis=1)
            energy_rate = np.sum(weights * tail * rate, axis=1)
            work = weights[0] * tail[:, 0] * group["input_coefficient"] * speed * driving
            loss = 2 * damping * energy + weights[-1] * group["terminal_coefficient"] / times * tail[:, -1] ** 2
            scale = max(float(np.max(abs(work))), float(np.max(abs(loss))), float(np.max(abs(energy_rate))), 1e-80)
            balance_error = float(np.max(abs(energy_rate - work + loss)) / scale)
            algebra_errors, return_errors, numerical_coefficients = [], [], []
            weighted_growth_rates = []
            for index, stamp in enumerate(audit["times"]):
                matrix = audit["matrices"][index]
                actual_speed = float(matrix[indices[0], low] / group["input_coefficient"])
                actual_opacity = 0. if group["massive"] else float(-matrix[indices[0], indices[0]])
                expected = actual_speed * group["streaming"] - actual_opacity * np.eye(len(indices))
                expected[-1, -1] -= group["terminal_coefficient"] / stamp
                actual = matrix[np.ix_(indices, indices)]
                algebra_errors.append(relative(actual, expected))
                input_row = matrix[np.ix_(indices, core_indices)]
                expected_input = np.zeros_like(input_row)
                expected_input[0, int(np.flatnonzero(core_indices == low)[0])] = actual_speed * group["input_coefficient"]
                algebra_errors.append(relative(input_row, expected_input))
                output_row = matrix[np.ix_(core_indices, indices)]
                expected_output = np.zeros_like(output_row)
                expected_output[int(np.flatnonzero(core_indices == low)[0]), 0] = actual_speed * group["output_coefficient"]
                return_errors.append(relative(output_row, expected_output))
                outside = np.array([position for position in tail_indices if position not in indices])
                require(np.count_nonzero(matrix[np.ix_(indices, outside)]) == 0, "cross-tail coupling")
                transformed = np.sqrt(weights[:, None] / weights[None, :]) * actual
                symmetric = (transformed + transformed.T) / 2
                weighted_growth_rates.append(float(np.linalg.eigvalsh(symmetric)[-1]))
                predicted_speed = float(1 / np.sqrt(1 + mass_ratio * (scale_curve(stamp) / scale_factor[0]) ** 2))
                numerical_coefficients.append(abs(predicted_speed - actual_speed) / actual_speed)
                if not group["massive"]:
                    numerical_coefficients.append(abs(float(opacity_curve(stamp)) - actual_opacity) / actual_opacity)
            norm = np.sqrt(2 * energy)
            bound = norm_bound(times, damping, speed, driving, reference["derivative"][:, low], norm[0], weights[0])
            quadrature = norm_bound(times, damping, speed, driving, reference["derivative"][:, low], norm[0], weights[0], order=8)
            coarse = norm_bound(times, damping, speed, driving, reference["derivative"][:, low], norm[0], weights[0], stride=2)
            containment = float(np.max(np.maximum(norm - bound, 0)) / max(float(np.max(norm)), 1e-80))
            independent = np.sqrt(np.sum(weights * full["state"][:, indices] ** 2, axis=1))
            tighter = np.sqrt(np.sum(weights * fine["state"][:, indices] ** 2, axis=1))
            output_magnitude = abs(group["output_coefficient"] * speed * tail[:, 0])
            output_bound = abs(group["output_coefficient"]) * speed * bound / np.sqrt(weights[0])
            group["speed_curve"] = PchipInterpolator(times, speed)
            report = dict(name=group["name"], tail_dimension=len(indices), low_native=int(reference["mapping"][low]), terminal_weight=float(weights[-1]), first_weight=float(weights[0]), minimum_speed=float(np.min(speed)), maximum_speed=float(np.max(speed)), minimum_damping=float(np.min(damping)),
                          energy_balance_error=balance_error, rate_error=relative(expected_rate, rate), operator_identity_error=max(algebra_errors), return_port_error=max(return_errors), independent_background_error=max(numerical_coefficients),
                          maximum_weighted_logarithmic_rate=max(weighted_growth_rates), growth_rates=weighted_growth_rates,
                          containment_error=containment, norm_quadrature_refinement=relative(quadrature, bound), norm_source_refinement=relative(coarse, bound), independent_norm_error=relative(independent, norm), norm_precision_error=relative(independent, tighter),
                          final_norm=float(norm[-1]), final_bound=float(bound[-1]), bound_to_norm_sup=float(np.max(bound) / max(float(np.max(norm)), 1e-80)), final_return=float(output_magnitude[-1]), final_return_bound=float(output_bound[-1]), initial_preparation_norm=float(norm[0]))
            report["passed"] = bool(max(report[key] for key in ("energy_balance_error", "rate_error", "containment_error", "norm_quadrature_refinement", "norm_source_refinement", "independent_norm_error", "norm_precision_error", "independent_background_error")) < GATE and max(algebra_errors + return_errors) < ALGEBRA)
            group_reports.append(report)
            path = model_root / (group["name"] + "-energy.npz")
            np.savez_compressed(path, times=times, indices=indices, weights=weights, norm=norm, bound=bound, quadrature_bound=quadrature, coarse_bound=coarse, energy=energy, energy_rate=energy_rate, work=work, loss=loss, speed=speed, damping=damping, return_magnitude=output_magnitude, return_bound=output_bound)
            report["file"], report["sha256"] = path.name, digest(path)
            all_rows.append(dict(model=model, **{key: value for key, value in report.items() if isinstance(value, (str, int, float, bool))}))
            print(model, group["name"], "energy", report["passed"], balance_error, report["norm_source_refinement"], flush=True)
        offsets = np.cumsum([0] + [len(group["indices"]) for group in groups])
        starting = np.zeros(len(tail_indices))
        starting[offsets[:-1]] = 1.
        last_guard = time.monotonic()
        def undamped_rhs(stamp, values):
            nonlocal last_guard
            if time.monotonic() - last_guard > 2:
                guard()
                last_guard = time.monotonic()
            result = np.empty_like(values)
            for group_index, group in enumerate(groups):
                selection = slice(offsets[group_index], offsets[group_index + 1])
                current = values[selection]
                speed_value = float(group["speed_curve"](stamp))
                result[selection] = speed_value * (group["streaming"] @ current)
                result[offsets[group_index + 1] - 1] -= group["terminal_coefficient"] / stamp * current[-1]
            return result
        for fraction in (0., .25, .5):
            release = lower + fraction * (upper - lower)
            output_times = np.unique(np.r_[release, times[reference["probes"]][times[reference["probes"]] >= release], upper])
            solutions = []
            for tolerance in (2e-11, 2e-12):
                guard()
                solution = solve_ivp(undamped_rhs, (release, upper), starting, method="DOP853", rtol=tolerance, atol=tolerance / 100, t_eval=output_times)
                require(solution.success, "tail impulse solver")
                solutions.append(solution.y.T)
            port_data, envelopes = [], []
            for index, group in enumerate(groups):
                selection = slice(offsets[index], offsets[index + 1])
                resolved = solutions[1][:, selection]
                norm_ratio = np.sqrt(np.sum(group["weights"] * resolved ** 2, axis=1) / group["weights"][0])
                attenuation = np.ones(len(output_times)) if group["massive"] else np.exp(-(optical(output_times) - optical(release)))
                initial_speed = float(group["speed_curve"](release))
                current_speed = group["speed_curve"](output_times)
                prefactor = group["output_coefficient"] * group["input_coefficient"] * current_speed * initial_speed
                kernel = prefactor * attenuation * resolved[:, 0]
                envelope = abs(prefactor) * attenuation
                refinement = relative(solutions[0][:, selection], resolved)
                growth = float(np.max(np.maximum(norm_ratio - 1, 0)))
                port_violation = float(np.max(np.maximum(abs(resolved[:, 0]) - 1, 0)))
                record = dict(group=group["name"], release_fraction=fraction, release=float(release), norm_excess=growth, returned_kernel_excess=port_violation, refinement=refinement, initial_kernel=float(kernel[0]), final_kernel=float(kernel[-1]), final_envelope=float(envelope[-1]), optical_depth=float(optical(upper) - optical(release)) if not group["massive"] else 0., passed=bool(max(growth, port_violation, refinement) < GATE))
                kernel_reports.append(record)
                port_data.append(kernel)
                envelopes.append(envelope)
            path = model_root / ("impulse-" + str(int(100 * fraction)) + ".npz")
            np.savez_compressed(path, times=output_times, undamped_base=solutions[0], undamped_fine=solutions[1], kernels=np.array(port_data).T, envelopes=np.array(envelopes).T, groups=np.array([group["name"] for group in groups]))
            print(model, "release", fraction, "complete", flush=True)
        passed = all(row["passed"] for row in group_reports + kernel_reports)
        report = dict(model=model, passed=passed, tail_dimension=len(tail_indices), retained_core_dimension=len(core_indices), groups=group_reports, kernels=kernel_reports, optical_depth=float(optical(upper) - optical(lower)), duration=float(upper - lower), massless_UFA_retained=True, physical_energy_density_claim=False, full_gravity_contraction_claim=False)
        write(model_root / "result.json", report)
        reports.append(report)
    with (ROOT / "tail-summary.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)
    result = dict(passed=all(row["passed"] for row in reports), reports=reports, symbolic=symbolic, source_sha256=digest(__file__), input_result_sha256=digest(ROOT / "input-result.json"), prior_result_sha256=digest(PRIOR / "comparison-result.json"), protocol_sha256=digest(ROOT / "PROTOCOL.md"), numerical_gate=GATE, algebra_gate=ALGEBRA, source_histories_reused=True, equation_or_bank_changes=False, numerical_evaluation_not_continuum_enclosure=True)
    write(ROOT / "tail-energy-result.json", result)
    require(result["passed"], "tail energy check failed; preserve and inspect")


if __name__ == "__main__":
    main()
