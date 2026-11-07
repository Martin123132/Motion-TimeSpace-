import ast
import time
from common import *
from native_context import factory
from rest_operator_v2 import NativeRest, JFULL, norm, sup
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline


def retained_observables():
    path = SECOND / "check_second.py"
    nodes = [node for node in ast.parse(path.read_text()).body if isinstance(node, ast.FunctionDef) and node.name in ("physical", "errors")]
    namespace = dict(np=np)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace["physical"], namespace["errors"]


def ratios(terms):
    values = np.asarray(terms)
    return sup(values.sum(axis=0)) / max(sup(values), 1e-30)


def main():
    modest()
    check_parent()
    require(read(ROOT / "preflight-v2-result.json")["passed"], "native feedback")
    coefficient_report = read(ROOT / "coefficient-result.json")
    require(coefficient_report["passed"] and digest(ROOT / "heavy-balanced-coefficients.npz") == coefficient_report["sha256"], "coefficient cache")
    (ROOT / "forward-contexts").mkdir(exist_ok=False)
    (ROOT / "forward").mkdir(exist_ok=False)
    frozen = {str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    write(ROOT / "forward-inputs.json", dict(sources=frozen, coefficient_sha256=coefficient_report["sha256"],
          rtol=2e-12, atol=2e-14, maximum_ell=192, galerkin=True, labels=["heavy-balanced", "cold-balanced"],
          cases=["full", "mean"], initial_data="same owned native seed; exact canonical map for mean; no constraint projection or fit",
          numerical=GATE, future_perturbation_sources=False))
    open_context = factory("forward-contexts")
    physical, errors = retained_observables()
    wave = dict(read(WAVELENGTH / "inventory-config.json")["waves"])["balanced"]
    coefficient_packet = load(ROOT / "heavy-balanced-coefficients.npz")
    interpolators = {name: CubicSpline(coefficient_packet["efold"], coefficient_packet[name], axis=0)
                     for name in ("hessian", "source", "feedback", "transform")}
    exact_map = load(TIMECHAIN / "operators/balanced.npz")
    exact_physical_rate = exact_map["rate"] * exact_map["balance"][:, :, None] / exact_map["balance"][:, None, :]
    reports = []
    for model in ("heavy", "cold"):
        guard()
        context = open_context(model, "balanced", wave)
        system = NativeRest(context, model, wave)
        grid = system.background["efold"]
        initial_state, initial_rest, _, _, _ = system.encode(float(grid[0]), context["reference"]["initial"])
        initial_units = context["normalization"]
        canonical_units = np.zeros(8)
        for index in range(system.dimension):
            basis = np.zeros(system.dimension)
            basis[index] = initial_units[index]
            canonical_units += abs(system.encode(float(grid[0]), basis)[0])
        canonical_units[canonical_units == 0] = 1.
        units = np.r_[canonical_units, system.rest_units]
        max_step = float(context["max_step"])
        first_step = min(context["old_first_step"] * context["point"](float(grid[0]))[12], max_step / 8)
        packets, rows = {}, []
        if model == "heavy":
            require(np.array_equal(grid, coefficient_packet["efold"]) and np.array_equal(grid, exact_map["efold"]), "physical grid")
        for case in ("full", "mean"):
            guard()
            initial = initial_state.copy()
            if model == "heavy" and case == "mean":
                initial = np.linalg.solve(coefficient_packet["transform"][0], initial)
            initial_vector = np.r_[initial, initial_rest]
            last_guard = time.monotonic()
            def derivative(efold, vector):
                state, rest = vector[:8], vector[8:]
                if model == "cold" or case == "full":
                    state_rate, rest_rate = system.full_rhs(efold, state, rest)
                else:
                    internal, linear, _, _ = system.source_only(efold, rest)
                    state_rate = JFULL @ (interpolators["hessian"](efold) @ state + interpolators["source"](efold) @ linear)
                    expansion, shear = interpolators["feedback"](efold) @ state
                    hubble = context["point"](efold)[12]
                    native_rest_rate = internal + (system.expansion[system.rest_positions] * expansion + system.shear[system.rest_positions] * shear) / hubble
                    rest_rate = system.extend_tail(efold, rest, native_rest_rate)
                return np.r_[state_rate, rest_rate]
            def rhs(efold, normalized):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                return derivative(efold, normalized * units) / units
            require(np.count_nonzero(derivative(float(grid[0]), np.zeros(len(units)))) == 0, "exact zero RHS")
            started = time.monotonic()
            print(model, case, "starting", len(units), "variables", flush=True)
            solution = solve_ivp(rhs, (float(grid[0]), float(grid[-1])), initial_vector / units,
                                 method="DOP853", rtol=2e-12, atol=2e-14, first_step=first_step, max_step=max_step, t_eval=grid)
            status = dict(success=bool(solution.success), message=solution.message, nfev=solution.nfev,
                          points=len(solution.t), last_efold=float(solution.t[-1]), seconds=time.monotonic() - started)
            write(ROOT / "forward" / (model + "-" + case + "-status.json"), status)
            require(solution.success and len(solution.t) == len(grid) and np.isfinite(solution.y).all(), "forward solve failed")
            evolved = solution.y.T * units
            state = evolved[:, :8].copy()
            if model == "heavy" and case == "mean":
                state = np.einsum("nij,nj->ni", coefficient_packet["transform"], evolved[:, :8])
            projected = np.empty((len(grid), system.dimension))
            observer = np.empty((len(grid), 30))
            metadata = np.empty((len(grid), 25))
            terms = np.empty((len(grid), 7, 7))
            rates = np.empty_like(state)
            canonical_geometry = np.empty((len(grid), 2))
            for index, efold in enumerate(grid):
                if index % 512 == 0:
                    guard()
                point = context["point"](float(efold))
                current_rate = derivative(float(efold), evolved[index])[:8]
                if model == "heavy" and case == "mean":
                    current_rate = coefficient_packet["transform"][index] @ current_rate + exact_physical_rate[index] @ evolved[index, :8]
                rates[index] = current_rate
                projected[index] = system.decode(float(efold), state[index], evolved[index, 8:])
                observer[index] = context["observe"](point[11], projected[index])
                terms[index], metadata[index] = context["stress"](point[11], projected[index])
                canonical_geometry[index] = system.geometry(float(efold), state[index])
            scale, hubble = observer[:, 27], observer[:, 28]
            current = terms[:, :, 1].sum(axis=1)
            density = terms[:, :, 0].sum(axis=1)
            z_kinematic = hubble * rates[:, 4] / (2 * wave)
            eta_kinematic = hubble * rates[:, 6]
            sigma_kinematic = z_kinematic + 3 * eta_kinematic / wave
            constraints = dict(
                Hamiltonian_canonical=ratios([wave**2 * state[:, 6], -hubble * wave * canonical_geometry[:, 0], density / 2]),
                momentum_canonical=ratios([state[:, 5] / scale**2, -terms[:, :5, 1].sum(axis=1) / (2 * wave)]),
                Hamiltonian_kinematic=ratios([wave**2 * state[:, 6], -hubble * wave * z_kinematic, density / 2]),
                momentum_kinematic=ratios([eta_kinematic, -current / (2 * wave)]),
                shear_velocity_difference=sup(sigma_kinematic - canonical_geometry[:, 1]) / max(norm(canonical_geometry[:, 1]), 1e-30))
            packet = dict(efold=grid, times=system.background["times"], a=scale, H=hubble, projected_state=projected,
                          observer=observer, observer_names=context["reference"]["observer_names"], metadata=metadata, terms=terms,
                          canonical_state=state, evolved_state=evolved, canonical_state_rate=rates, canonical_geometry=canonical_geometry,
                          z_kinematic=z_kinematic, sigma_kinematic=sigma_kinematic, units=units, mapping=system.mapping)
            path = ROOT / "forward" / (model + "-" + case + ".npz")
            np.savez_compressed(path, **packet)
            row = dict(model=model, case=case, status=status, packet=str(path), sha256=digest(path), constraints=constraints,
                       constraints_passed=max(constraints.values()) < GATE)
            rows.append(row)
            packets[case] = packet
            print(model, case, "saved", status, constraints, flush=True)
            del solution, evolved
        owner = next(family for family in read(SECOND / "prediction-result.json")["reports"] if family["model"] == model and family["label"] == "balanced")
        reference_case = next(case for case in owner["cases"] if case["tag"] == "G192-full-fine")
        reference_path = SECOND / "runs-second" / (model + "-balanced") / reference_case["file"]
        require(digest(reference_path) == reference_case["sha256"], "comparison reference integrity")
        reference = load(reference_path)
        require(np.array_equal(reference["efold"], grid), "reference grid")
        values = {name: physical(packet, wave) for name, packet in packets.items()}
        values["native"] = physical(reference, wave)
        comparisons = []
        for left, right in (("full", "native"), ("mean", "native"), ("mean", "full")):
            target = reference if right == "native" else packets[right]
            state_error = float(np.max(errors(packets[left]["projected_state"], target["projected_state"])))
            signals = {name: float(errors(values[left][name], values[right][name])) for name in values[left] if name not in ("a", "H", "R", "Phi_rate")}
            comparisons.append(dict(left=left, right=right, state_error=state_error, physical_errors=signals,
                                    passed=max(state_error, *signals.values()) < GATE))
        report = dict(model=model, label="balanced", wave=wave, rows=rows, comparisons=comparisons,
                      all_passed=all(row["constraints_passed"] for row in rows) and all(row["passed"] for row in comparisons),
                      interpretation="native-observer physical regression accompanied by separately computed canonical and kinematic constraints",
                      future_sources_used=False, independent_forward=True)
        write(ROOT / "forward" / (model + "-result.json"), report)
        reports.append(report)
        print(model, "comparisons", comparisons, "passed", report["all_passed"], flush=True)
        del packets, reference, context, system
    check_parent()
    write(ROOT / "forward-result.json", dict(state="complete", passed=all(row["all_passed"] for row in reports), reports=reports,
          prospective_equations=True, current_state_rest_feedback=True, no_future_sources=True, further_wavelengths_started=False))
    print("Forward comparisons completed", flush=True)


if __name__ == "__main__":
    main()
