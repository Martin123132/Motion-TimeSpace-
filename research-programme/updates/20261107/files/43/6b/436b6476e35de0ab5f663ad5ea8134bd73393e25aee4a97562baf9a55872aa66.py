import time
from common import *
from corrector_v2 import *
from forward import retained_observables, ratios
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


def main():
    modest()
    check_parent()
    qualification = read(ROOT / "assembly-result.json")
    require(qualification["passed"] and digest(ROOT / "coupled-factors.npz") == qualification["packet_sha256"], "corrector representation")
    frozen = {str(path): digest(path) for path in STAGE.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    write(ROOT / "evolution-inputs.json", dict(sources=frozen, factor_sha256=qualification["packet_sha256"],
          rtol=2e-12, atol=2e-14, maximum_ell=192, numerical=GATE, algebra=ALGEBRA,
          cases={"heavy": ["full", "exact", "corrected"], "cold": ["full", "corrected"]}, label=LABEL,
          future_perturbation_sources=False, initial_data="same original seed through exact S and Schur inverse",
          corrected_generator="M+M U-U M0-U_N; full derivative; no further phase projection"))
    (ROOT / "evolution").mkdir(exist_ok=False)
    (ROOT / "evolution-contexts").mkdir(exist_ok=False)
    open_context = factory("evolution-contexts")
    physical, errors = retained_observables()
    packet = load(ROOT / "coupled-factors.npz")
    correction = HigherOrderCorrector(packet)
    wave = float(packet["wave"])
    coefficient_packet = packet
    mean_coefficients = {name: CubicSpline(coefficient_packet["efold"], coefficient_packet[name], axis=0)
                         for name in ("hessian", "source", "feedback")}
    exact_map = load(TIMECHAIN / "operators" / (LABEL + ".npz"))
    exact_physical_rate = exact_map["rate"] * exact_map["balance"][:, :, None] / exact_map["balance"][:, None, :]
    reports = []
    for model in ("heavy", "cold"):
        guard()
        context = open_context(model, LABEL, wave)
        system = NativeRest(context, model, wave)
        grid = system.background["efold"]
        initial_state, initial_rest, _, _, _ = system.encode(float(grid[0]), context["reference"]["initial"])
        canonical_units = np.zeros(8)
        for index in range(system.dimension):
            basis = np.zeros(system.dimension)
            basis[index] = context["normalization"][index]
            canonical_units += abs(system.encode(float(grid[0]), basis)[0])
        canonical_units[canonical_units == 0] = 1.
        units = np.r_[canonical_units, system.rest_units]
        if model == "heavy":
            require(np.array_equal(units, packet["units"]) and np.array_equal(grid, packet["efold"]), "identical original state units and grid")
        max_step = float(context["max_step"])
        first_step = min(context["old_first_step"] * context["point"](float(grid[0]))[12], max_step / 8)
        max_norm, max_identity, max_generator_defect = 0., 0., 0.
        def operators(efold):
            nonlocal max_norm
            ub = correction.blocks(efold)
            vb = correction.blocks(efold, "V")
            db = correction.blocks(efold, "U", 1)
            current_norm = infinity_norm(ub, units, correction.support, correction.vectors)
            max_norm = max(max_norm, current_norm)
            require(current_norm < 1, "runtime inverse gate")
            mean_hessian = mean_coefficients["hessian"](efold)
            mean_source = mean_coefficients["source"](efold)
            mean_feedback = mean_coefficients["feedback"](efold)
            hubble = context["point"](efold)[12]
            def mean_action(vector):
                state, rest = vector[:8], vector[8:]
                internal, linear, _, _ = system.source_only(efold, rest)
                state_rate = JFULL @ (mean_hessian @ state + mean_source @ linear)
                rest_rate = internal + correction.vectors[:system.native_rest_size] @ (mean_feedback @ state) / hubble
                return np.r_[state_rate, system.extend_tail(efold, rest, rest_rate)]
            def apply_block(blocks, vector):
                return apply(blocks, vector, correction.support, correction.vectors)
            return ub, vb, db, mean_action, apply_block
        if model == "heavy":
            for probe_index in np.unique(np.linspace(0, len(grid) - 1, 17, dtype=int)):
                efold = float(grid[probe_index])
                ub, vb, db, mean_action, apply_block = operators(efold)
                probe = np.sin(np.arange(len(units)) + probe_index + 1.) * units
                mean_rate = mean_action(probe)
                uvalue = apply_block(ub, probe)
                rate = mean_rate + apply_block(vb, probe) + mean_action(uvalue) + apply_block(vb, uvalue) - apply_block(ub, mean_rate) - apply_block(db, probe)
                exact_physical = mean_action(probe + uvalue) + apply_block(vb, probe + uvalue)
                reconstructed_rate = rate + apply_block(ub, rate) + apply_block(db, probe)
                predicted_defect = apply_block(ub, rate - mean_rate)
                denominator = max(np.max(abs(exact_physical / units)), 1e-80)
                max_identity = max(max_identity, float(np.max(abs((reconstructed_rate - exact_physical - predicted_defect) / units)) / denominator))
                max_generator_defect = max(max_generator_defect, float(np.max(abs(predicted_defect / units)) / denominator))
            require(max_identity < ALGEBRA, "first corrected generator identity")
        cases = ("full", "exact", "corrected") if model == "heavy" else ("full", "corrected")
        packets, rows = {}, []
        for case in cases:
            guard()
            initial = np.r_[initial_state, initial_rest]
            if model == "heavy" and case != "full":
                initial[:8] = np.linalg.solve(coefficient_packet["transform"][0], initial[:8])
                initial = correction.inverse(float(grid[0]), initial)
            def derivative(efold, vector):
                if model == "cold" or case == "full":
                    return np.concatenate(system.full_rhs(efold, vector[:8], vector[8:]))
                ub, vb, db, mean_action, apply_block = operators(efold)
                uvalue = apply_block(ub, vector)
                dvalue = apply_block(db, vector)
                if case == "exact":
                    transformed = vector + uvalue
                    original_rate = mean_action(transformed) + apply_block(vb, transformed)
                    return inverse(ub, original_rate - dvalue, correction.support, correction.vectors)
                mean_rate = mean_action(vector)
                return mean_rate + apply_block(vb, vector) + mean_action(uvalue) + apply_block(vb, uvalue) - apply_block(ub, mean_rate) - dvalue
            require(np.count_nonzero(derivative(float(grid[0]), np.zeros(len(units)))) == 0, "exact zero RHS")
            last_guard = time.monotonic()
            def rhs(efold, normalized):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                return derivative(efold, normalized * units) / units
            started = time.monotonic()
            print(model, case, "starting", len(units), "variables", flush=True)
            solution = solve_ivp(rhs, (float(grid[0]), float(grid[-1])), initial / units, method="DOP853",
                                 rtol=2e-12, atol=2e-14, first_step=first_step, max_step=max_step, t_eval=grid)
            status = dict(success=bool(solution.success), message=solution.message, nfev=solution.nfev,
                          points=len(solution.t), last_efold=float(solution.t[-1]), seconds=time.monotonic() - started)
            write(ROOT / "evolution" / (model + "-" + case + "-status.json"), status)
            require(solution.success and len(solution.t) == len(grid) and np.isfinite(solution.y).all(), "forward solve failed")
            evolved = solution.y.T * units
            state = np.empty((len(grid), 8))
            rates = np.empty_like(state)
            projected = np.empty((len(grid), system.dimension))
            observer = np.empty((len(grid), 30))
            metadata = np.empty((len(grid), 25))
            terms = np.empty((len(grid), 7, 7))
            canonical_geometry = np.empty((len(grid), 2))
            remainder = np.zeros(len(grid))
            for index, efold in enumerate(grid):
                if index % 512 == 0:
                    guard()
                efold = float(efold)
                point = context["point"](efold)
                vector = evolved[index]
                rate = derivative(efold, vector)
                if model == "heavy" and case != "full":
                    ub, vb, db, mean_action, apply_block = operators(efold)
                    transformed = vector + apply_block(ub, vector)
                    physical_rate = rate + apply_block(ub, rate) + apply_block(db, vector)
                    state[index] = coefficient_packet["transform"][index] @ transformed[:8]
                    rates[index] = coefficient_packet["transform"][index] @ physical_rate[:8] + exact_physical_rate[index] @ transformed[:8]
                    rest = transformed[8:]
                    if case == "corrected":
                        defect = apply_block(ub, rate - mean_action(vector))
                        denominator = max(np.max(abs((mean_action(transformed) + apply_block(vb, transformed)) / units)), 1e-80)
                        remainder[index] = np.max(abs(defect / units)) / denominator
                else:
                    state[index], rates[index], rest = vector[:8], rate[:8], vector[8:]
                projected[index] = system.decode(efold, state[index], rest)
                observer[index] = context["observe"](point[11], projected[index])
                terms[index], metadata[index] = context["stress"](point[11], projected[index])
                canonical_geometry[index] = system.geometry(efold, state[index])
            scale_value, hubble = observer[:, 27], observer[:, 28]
            current, density = terms[:, :, 1].sum(axis=1), terms[:, :, 0].sum(axis=1)
            z_kinematic = hubble * rates[:, 4] / (2 * wave)
            eta_kinematic = hubble * rates[:, 6]
            sigma_kinematic = z_kinematic + 3 * eta_kinematic / wave
            constraints = dict(
                Hamiltonian_canonical=ratios([wave**2 * state[:, 6], -hubble * wave * canonical_geometry[:, 0], density / 2]),
                momentum_canonical=ratios([state[:, 5] / scale_value**2, -terms[:, :5, 1].sum(axis=1) / (2 * wave)]),
                Hamiltonian_kinematic=ratios([wave**2 * state[:, 6], -hubble * wave * z_kinematic, density / 2]),
                momentum_kinematic=ratios([eta_kinematic, -current / (2 * wave)]),
                shear_velocity_difference=float(np.max(abs(sigma_kinematic - canonical_geometry[:, 1]))) / max(float(np.max(abs(canonical_geometry[:, 1]))), 1e-30))
            output = dict(efold=grid, times=system.background["times"], a=scale_value, H=hubble, projected_state=projected,
                          observer=observer, observer_names=context["reference"]["observer_names"], metadata=metadata, terms=terms,
                          canonical_state=state, evolved_state=evolved, canonical_state_rate=rates, canonical_geometry=canonical_geometry,
                          z_kinematic=z_kinematic, sigma_kinematic=sigma_kinematic, units=units, mapping=system.mapping, remainder=remainder)
            path = ROOT / "evolution" / (model + "-" + case + ".npz")
            np.savez_compressed(path, **output)
            rows.append(dict(model=model, case=case, status=status, packet=str(path), sha256=digest(path), constraints=constraints,
                             constraints_passed=max(constraints.values()) < GATE, maximum_generator_remainder=float(np.max(remainder))))
            packets[case] = output
            print(model, case, "saved", status, constraints, flush=True)
            del solution, evolved
        parent_report = next(report for report in read(SECOND / "prediction-result.json")["reports"] if report["model"] == model and report["label"] == LABEL)
        parent_case = next(row for row in parent_report["cases"] if row["tag"] == "G192-full-fine")
        reference_path = SECOND / "runs-second" / (model + "-" + LABEL) / parent_case["file"]
        require(digest(reference_path) == parent_case["sha256"], "native full control")
        packets["native"] = load(reference_path)
        require(np.array_equal(grid, packets["native"]["efold"]), "full-control grid")
        values = {name: physical(packet, wave) for name, packet in packets.items()}
        pairs = [(case, "native") for case in cases] + [("corrected", "full")]
        if model == "heavy":
            pairs += [("exact", "full"), ("corrected", "exact")]
        comparisons = []
        for left, right in pairs:
            state_error = float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))
            signals = {name: float(errors(values[left][name], values[right][name])) for name in values[left] if name not in ("a", "H", "R", "Phi_rate")}
            comparisons.append(dict(left=left, right=right, state_error=state_error, physical_errors=signals, passed=max(state_error, *signals.values()) < GATE))
        report = dict(model=model, label=LABEL, wave=wave, rows=rows, comparisons=comparisons, independent_forward=True, future_sources_used=False,
                      maximum_encountered_U=max_norm, generator_identity_error=max_identity, random_probe_generator_defect=max_generator_defect,
                      all_passed=all(row["constraints_passed"] for row in rows) and all(row["passed"] for row in comparisons))
        write(ROOT / "evolution" / (model + "-result.json"), report)
        reports.append(report)
        print(model, "comparisons", comparisons, "passed", report["all_passed"], flush=True)
        del packets, values, context, system
    check_parent()
    write(ROOT / "evolution-result.json", dict(state="complete", passed=all(row["all_passed"] for row in reports), reports=reports,
          original_mean_failure_preserved=True, tested_label=LABEL, new_evolutions=5,
          exact_case_is_coordinate_control=True, corrected_case_has_explicit_generator_remainder=True))
    print("Coupled phase-corrector forward test complete", flush=True)


if __name__ == "__main__":
    main()

