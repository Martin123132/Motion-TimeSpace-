from common import *
from poisson_driver import *
from forward import retained_observables
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
import time
import numpy as np

BRANCHES = ("gr", "poisson-spatial", "newton-dust-force")
NAMES = ("Phi", "Psi", "D", "Q", "Pi", "theta_c", "delta_c", "delta_b", "delta_gamma", "delta_massless")


def sup(value):
    return float(np.max(abs(np.asarray(value))))


def relative(value, scale):
    return sup(value) / max(sup(scale), 1e-80)


def identity(*terms):
    return relative(np.sum(terms, axis=0), np.asarray(terms))


def compare(packet, control, wave):
    values = {name: packet["values"][:, index] for index, name in enumerate(NAMES)}
    reference = {name: control["values"][:, index] for index, name in enumerate(NAMES)}
    difference = {name: values[name] - reference[name] for name in NAMES}
    report = {name: relative(difference[name], reference[name]) for name in NAMES}
    hubble, scale = packet["H"], packet["a"]
    feedback = -difference["D"] / (2 * wave**2)
    dropped_momentum = 3 * hubble * reference["Q"] / (2 * wave**3)
    dropped_shear = reference["Pi"] / wave**2
    decomposition = relative(difference["Psi"] - feedback - dropped_momentum - dropped_shear, reference["Psi"])
    rows = []
    for stride in (1, 2):
        keep = np.unique(np.r_[np.arange(0, len(scale), stride), len(scale) - 1])
        times = packet["times"]
        velocity_integral = CubicSpline(times[keep], (scale * difference["Psi"])[keep]).antiderivative()
        velocity_change = (scale[0] * difference["theta_c"][0] + wave**2 * (velocity_integral(times) - velocity_integral(times[0]))) / scale
        density_integral = CubicSpline(times[keep], difference["theta_c"][keep]).antiderivative()
        density_change = difference["delta_c"][0] - density_integral(times) + density_integral(times[0])
        density_change += 3 * (difference["Phi"] - difference["Phi"][0])
        rows.append(dict(stride=stride, velocity=relative(velocity_change - difference["theta_c"], reference["theta_c"]),
                         density=relative(density_change - difference["delta_c"], reference["delta_c"])))
    return dict(physical_errors=report,
                final_relative={name: float(difference[name][-1]) / max(sup(reference[name]), 1e-80) for name in NAMES},
                force_feedback=relative(feedback, reference["Psi"]),
                removed_control_momentum=relative(dropped_momentum, reference["Psi"]),
                removed_control_shear=relative(dropped_shear, reference["Psi"]),
                force_decomposition=decomposition, live_evolution_integral_checks=rows,
                spatial_phi_is_driver_only=packet["branch"].item() == "newton-dust-force")


def main():
    modest()
    check_parent()
    preflight = ROOT / "preflight-v2"
    require(read(preflight / "preflight-result.json")["passed"], "preflight")
    for path, expected in read(preflight / "frozen-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen source: " + path)
    frozen = {str(path): digest(path) for path in STAGE.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    write(ROOT / "evolution-v2-inputs.json", dict(sources=frozen, branches=BRANCHES, rtol=2e-12, atol=2e-14,
          algebra=ALGEBRA, numerical=GATE, maximum_ell=192, same_background_grid=True,
          future_perturbation_sources=False, physical_truncation_has_no_fake_numerical_acceptance_gate=True))
    destination = ROOT / "evolution"
    if destination.exists():
        require(LABEL == "half" and not any(destination.iterdir()), "only inspected empty setup-failure destination may continue")
        receipt = read(ROOT / "evolution-01.end.json")
        require(receipt["exit_code"] == 1 and "NameError: name 'np' is not defined" in (ROOT / "evolution-01.stderr.log").read_text(), "inspected setup failure")
    else:
        destination.mkdir(exist_ok=False)
    (ROOT / "evolution-contexts-v2").mkdir(exist_ok=False)
    physical, errors = retained_observables()
    reports = []
    for model in ("heavy", "cold"):
        system = open_system(model, "evolution-contexts-v2")
        context, wave = system.context, system.wave
        background = load(preflight / "backgrounds" / (model + ".npz"))
        require(digest(preflight / "backgrounds" / (model + ".npz")) == read(preflight / (model + "-preflight.json"))["units_sha256"], "qualified background")
        system.install_background(background)
        grid = system.background["efold"]
        require(np.array_equal(grid, background["efold"]), "original grid")
        max_step = float(context["max_step"])
        first_step = min(context["old_first_step"] * context["point"](float(grid[0]))[12], max_step / 8)
        packets, model_rows = {}, []
        for branch in BRANCHES:
            guard()
            last_guard = time.monotonic()
            def rhs(efold, normalized):
                nonlocal last_guard
                if time.monotonic() - last_guard > 2:
                    guard()
                    last_guard = time.monotonic()
                return system.evaluate(efold, normalized * system.units, branch)[0] / system.units
            print(model, branch, "starting", len(grid), "output nodes", flush=True)
            started = time.monotonic()
            solution = solve_ivp(rhs, (float(grid[0]), float(grid[-1])), system.initial / system.units,
                                 method="DOP853", rtol=2e-12, atol=2e-14, t_eval=grid,
                                 first_step=first_step, max_step=max_step)
            status = dict(success=bool(solution.success), message=solution.message, nfev=solution.nfev,
                          points=len(solution.t), seconds=time.monotonic() - started)
            write(ROOT / "evolution" / (model + "-" + branch + "-status.json"), status)
            require(solution.success and len(solution.t) == len(grid) and np.isfinite(solution.y).all(), "forward solve")
            evolved = solution.y.T * system.units
            values = np.empty((len(grid), len(NAMES)))
            projected = np.empty((len(grid), context["dimension"]))
            terms = np.empty((len(grid), 7, 7))
            diagnostics = np.empty((len(grid), 7))
            rates = np.empty((len(grid), 5))
            for index, efold in enumerate(grid):
                if index % 512 == 0:
                    guard()
                derivative, observables, rates_map, info, projected[index], terms[index] = system.evaluate(float(efold), evolved[index], branch)
                values[index] = [observables[name] for name in NAMES]
                rates[index] = [rates_map[name] for name in ("density_sync", "delta_c", "theta_c", "eta", "Phi")]
                diagnostics[index] = [info[name] for name in ("H", "scale", "enthalpy", "quadrature_enthalpy", "denominator", "z", "alpha")]
            packet = dict(efold=grid, times=system.background["times"], values=values, value_names=np.array(NAMES),
                          rates=rates, diagnostics=diagnostics, H=diagnostics[:, 0], a=diagnostics[:, 1],
                          projected_state=projected, evolved_state=evolved, units=system.units, terms=terms,
                          branch=np.array(branch), wave=np.array(wave), initial_raw=system.initial_raw)
            path = ROOT / "evolution" / (model + "-" + branch + ".npz")
            np.savez_compressed(path, **packet)
            current = {name: values[:, index] for index, name in enumerate(NAMES)}
            algebra = dict(continuity=identity(rates[:, 1], current["theta_c"], -3 * rates[:, 4]),
                           euler=identity(rates[:, 2], packet["H"] * current["theta_c"], -wave**2 * current["Psi"]))
            constraints = {}
            if branch == "gr":
                constraints = dict(Hamiltonian=identity(2 * wave**2 * current["Phi"], current["D"], 3 * packet["H"] * current["Q"] / wave),
                                   slip=identity(current["Phi"], -current["Psi"], -current["Pi"] / wave**2),
                                   momentum=identity(rates[:, 4], packet["H"] * current["Psi"], -current["Q"] / (2 * wave)))
            else:
                algebra["poisson"] = identity(2 * wave**2 * current["Psi"], current["D"])
                if branch == "newton-dust-force":
                    algebra["dust_continuity"] = identity(rates[:, 1], current["theta_c"])
            row = dict(model=model, branch=branch, packet=str(path), sha256=digest(path), status=status, algebra=algebra,
                       constraints=constraints, denominator_min=float(np.min(diagnostics[:, 4])),
                       background_H_over_k_max=sup(packet["H"]) / wave,
                       enthalpy_quadrature_defect=relative(diagnostics[:, 3] - diagnostics[:, 2], diagnostics[:, 2]),
                       current_state_omitted_momentum=relative(3 * packet["H"] * current["Q"] / (2 * wave**3), current["Psi"]),
                       current_state_omitted_shear=relative(current["Pi"] / wave**2, current["Psi"]),
                       radiation_sync_density_fraction=relative(terms[:, 2:4, 0].sum(axis=1), terms[:, :, 0].sum(axis=1)),
                       pressure_sync_fraction=relative(terms[:, :, 2].sum(axis=1), terms[:, :, 0].sum(axis=1)),
                       spatial_phi_is_driver_only=branch == "newton-dust-force")
            if branch == "gr":
                parent_case = next(item for report in read(REFERENCE_ROOT / "evolution-result.json")["reports"] if report["model"] == model
                                   for item in report["rows"] if item["case"] == "full")
                require(digest(parent_case["packet"]) == parent_case["sha256"], "retained full control")
                control = load(parent_case["packet"])
                require(np.array_equal(grid, control["efold"]), "control grid")
                reference = physical(control, wave)
                row["control"] = dict(state_error=float(np.max(errors(projected, control["projected_state"]))),
                                     physical_errors={name: relative(current[name] - reference[name], reference[name]) for name in NAMES},
                                     path=parent_case["packet"], sha256=parent_case["sha256"])
                row["control_passed"] = max(row["control"]["state_error"], *row["control"]["physical_errors"].values(), *constraints.values()) < GATE
            else:
                row["comparison"] = compare(packet, packets["gr"], wave)
                row["initial_matter_difference"] = {name: float(abs(current[name][0] - packets["gr"]["values"][0, NAMES.index(name)]))
                                                    for name in NAMES if name not in ("Phi", "Psi")}
            row["numerical_passed"] = bool(max(algebra.values()) < ALGEBRA and row.get("control_passed", True))
            write(ROOT / "evolution" / (model + "-" + branch + "-result.json"), row)
            print(model, branch, "saved", status, "numerical", row["numerical_passed"], flush=True)
            require(row["numerical_passed"], "inspect failed evolution gate before continuing")
            packets[branch] = packet
            model_rows.append(row)
            del solution
        report = dict(model=model, rows=model_rows, all_numerical_passed=all(row["numerical_passed"] for row in model_rows))
        write(ROOT / "evolution" / (model + "-result.json"), report)
        reports.append(report)
        del packets, system, context
    check_parent()
    write(ROOT / "evolution-result.json", dict(passed=True, reports=reports,
          independent_current_state_gravity=True, no_future_perturbation_sources=True,
          newton_scope="dust-force reduction with live relativistic species; Phi is a driver in chi=0"))
    print("six independent evolutions complete", flush=True)


if __name__ == "__main__":
    main()
