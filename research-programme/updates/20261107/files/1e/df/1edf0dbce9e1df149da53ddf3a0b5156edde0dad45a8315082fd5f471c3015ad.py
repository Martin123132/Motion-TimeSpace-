from common import *
from adjoint_operator import *
from compact_adjoint import CompactAdjoint
from source_split import physical_sources
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline, make_interp_spline
import time


from quadrature_v2 import integrate_budget, unit_checks

RUN = ROOT / "response-v2"


def main():
    modest()
    check_parent()
    RUN.mkdir(exist_ok=False)
    write(RUN / "quadrature-tests.json", unit_checks())
    build = read(ROOT / "build-result.json")
    require(build["passed"], "qualified coefficients")
    for path, expected in read(ROOT / "frozen-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen build input")
    write(RUN / "adjoint-inputs.json", dict(sources={str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")},
          rtol=2e-12, atol=2e-14, branches=BRANCHES, step_factors=[1., .5], numerical=GATE, algebra=ALGEBRA,
          targets=["D", "delta_c"], target_history_not_used_in_prediction=True, statistical_holdout_claimed=False))
    (ROOT / "adjoint-contexts-v2").mkdir(exist_ok=False)
    (RUN / "adjoints").mkdir(exist_ok=False)
    reports = []
    for model_report in build["reports"]:
        model = model_report["model"]
        require(digest(model_report["packet"]) == model_report["sha256"], "operator packet")
        packet = load(model_report["packet"])
        operator = CompactAdjoint(packet)
        grid = packet["efold"]
        system = open_owned(model, "adjoint-contexts-v2")
        context = system.context
        require(np.array_equal(system.units, packet["units"]), "fixed normalization")
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        reference_row = read(POISSON / "evolution" / (model + "-gr-result.json"))
        require(digest(reference_path) == reference_row["sha256"], "GR reference")
        reference = load(reference_path)
        require(np.array_equal(grid, reference["efold"]), "original reference grid")
        core_reference = reference["evolved_state"][:, :operator.size] / operator.units[:operator.size]
        value_names = reference["value_names"].tolist()
        output_reference = reference["values"][:, [value_names.index("D"), value_names.index("delta_c")]]
        output_scales = np.max(abs(output_reference), axis=0)
        require(np.min(output_scales) > 0, "nonzero fixed readout envelope")
        reference_spline = make_interp_spline(grid, core_reference, k=5, axis=0)
        source_channels = np.einsum("nbci,ni->nbc", packet["channels"], core_reference)
        terminal = np.zeros((operator.dimension, 2))
        terminal[:operator.size] = packet["rows"][-1].T / output_scales
        adjoint_scales = np.max(abs(terminal), axis=0)
        require(np.min(adjoint_scales) > 0, "adjoint initial scale")
        maximum_step = float(context["max_step"])
        first_step = min(context["old_first_step"] * context["point"](float(grid[0]))[12], maximum_step / 8)
        numerical = {}
        physical_split, split_errors = physical_sources(system, reference, source_channels)
        np.savez_compressed(RUN / "adjoints" / (model + "-physical-sources.npz"), efold=grid, **physical_split)
        for probe, index in enumerate(np.unique(np.linspace(2, len(grid) - 4, 33, dtype=int))):
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            state = np.zeros(operator.dimension)
            state[:operator.size] = reference_spline(efold)
            direct_gr = system.evaluate(efold, state * operator.units, "gr")
            for branch, label in enumerate(BRANCHES):
                direct = system.evaluate(efold, state * operator.units, label)
                actual = operator.splines["injection"](efold) @ (operator.splines["channels"](efold)[branch] @ state[:operator.size])
                expected = (direct[0] - direct_gr[0])[:operator.size] / operator.units[:operator.size]
                numerical[label + "_reference_residual"] = max(numerical.get(label + "_reference_residual", 0.), relative(actual - expected, expected))
            interpolated = operator.splines["base"](float(grid[index]))
            numerical["lossless_zero_compression"] = max(numerical.get("lossless_zero_compression", 0.), relative(interpolated - packet["base"][index], packet["base"][index]))
        require(max(numerical.values()) < GATE, "reference residual and compact coefficients")
        branch_rows = []
        del reference
        for branch, label in enumerate(BRANCHES):
            histories = []
            case_rows = []
            for factor, tag in ((1., "cap"), (.5, "half-cap")):
                guard()
                last_guard = time.monotonic()
                def rhs(efold, flattened):
                    nonlocal last_guard
                    if time.monotonic() - last_guard > 2:
                        guard()
                        last_guard = time.monotonic()
                    adjoint = flattened.reshape(operator.dimension, 2)
                    return -operator.apply(efold, adjoint, branch, transpose=True).ravel()
                prefix = model + "-" + label + "-" + tag
                reused = model == "heavy" and label == "poisson-spatial"
                if reused:
                    retained_row = read(ROOT / "adjoints" / (prefix + "-prediction.json"))
                    retained_path = Path(retained_row["packet"])
                    require(digest(retained_path) == retained_row["sha256"], "retained adjoint hash")
                    retained = load(retained_path)
                    require(np.array_equal(grid, retained["efold"]) and np.array_equal(terminal, retained["terminal_adjoint"]), "retained adjoint contract")
                    core = retained["adjoint_core"]
                    initial = retained["initial_adjoint"]
                    status = dict(retained_row["status"], reused_existing_solution=True, source_packet=str(retained_path))
                    print(prefix, "reusing completed adjoint; reprocessing only", flush=True)
                else:
                    started = time.monotonic()
                    print(model, label, tag, "backward adjoint starting", flush=True)
                    solution = solve_ivp(rhs, (float(grid[-1]), float(grid[0])), (terminal / adjoint_scales).ravel(),
                                         method="DOP853", rtol=2e-12, atol=2e-14, first_step=first_step * factor,
                                         max_step=maximum_step * factor, t_eval=grid[::-1])
                    status = dict(success=bool(solution.success), message=solution.message, nfev=solution.nfev,
                                  points=len(solution.t), seconds=time.monotonic() - started, max_step=maximum_step * factor)
                    prefix = model + "-" + label + "-" + tag
                    require(solution.success and len(solution.t) == len(grid) and np.isfinite(solution.y).all(), "adjoint evolution")
                    full = solution.y.T[::-1].reshape(len(grid), operator.dimension, 2)
                    core = full[:, :operator.size].copy() * adjoint_scales
                    initial = full[0].copy() * adjoint_scales
                write(RUN / "adjoints" / (prefix + "-status.json"), status)
                gains = np.einsum("nio,nic->noc", core, packet["injection"])
                contributions = gains * source_channels[:, branch, None, :]
                common_gain = gains[:, :, 0] + physical_split["mixing"][:, branch, None] * gains[:, :, 1]
                physical_contributions = np.stack([common_gain * physical_split["momentum"][:, None],
                                                   common_gain * physical_split["shear"][:, None],
                                                   gains[:, :, 1] * physical_split["temporal"][:, branch, None]], axis=2)
                require(relative(physical_contributions.sum(axis=2) - contributions.sum(axis=2), contributions) < ALGEBRA, "physical adjoint integrand split")
                physical_budgets = [integrate_budget(grid, physical_contributions, stride) for stride in (1, 2)]
                gain_channels = np.stack([common_gain, gains[:, :, 1]], axis=2)
                gain_budgets = [integrate_budget(grid, gain_channels, stride) for stride in (1, 2)]
                source_envelopes = np.array([sup(physical_split["momentum"]), sup(physical_split["shear"]), sup(physical_split["temporal"][:, branch])])
                gain_integrals = np.asarray(gain_budgets[0]["channel_absolute_budgets"])
                envelope_budget = gain_integrals[:, 0] * (source_envelopes[0] + source_envelopes[1]) + gain_integrals[:, 1] * source_envelopes[2]
                budgets = [integrate_budget(grid, contributions, stride) for stride in (1, 2)]
                if reused:
                    out = retained_path
                    require(np.array_equal(contributions, retained["contributions"]) and np.array_equal(physical_contributions, retained["physical_contributions"]), "reuse integrands exactly")
                else:
                    out = RUN / "adjoints" / (prefix + ".npz")
                    np.savez_compressed(out, efold=grid, adjoint_core=core, initial_adjoint=initial, terminal_adjoint=terminal,
                                        contributions=contributions, physical_contributions=physical_contributions, gain_channels=gain_channels,
                                        source_envelopes=source_envelopes, output_scales=output_scales, adjoint_scales=adjoint_scales)
                row = dict(tag=tag, status=status, packet=str(out), sha256=digest(out), budgets=budgets, physical_budgets=physical_budgets,
                           gain_budgets=gain_budgets, envelope_budget=envelope_budget.tolist(), source_envelopes=source_envelopes.tolist())
                write(RUN / "adjoints" / (prefix + "-prediction.json"), row)
                case_rows.append(row)
                histories.append((core, contributions))
                print(prefix, "saved prediction", budgets[0], flush=True)
                if not reused:
                    del full, solution
            fine = case_rows[1]["budgets"][0]
            prediction = np.array(fine["signed_prediction"])
            bound = np.array(fine["combined_absolute_budget"])
            coarse_prediction = np.array(case_rows[0]["budgets"][0]["signed_prediction"])
            coarse_bound = np.array(case_rows[0]["budgets"][0]["combined_absolute_budget"])
            refinement = dict(adjoint_core=relative(histories[0][0] - histories[1][0], histories[1][0]),
                              source_integrand=relative(histories[0][1] - histories[1][1], histories[1][1]),
                              signed_prediction=sup(prediction - coarse_prediction),
                              budget=relative(bound - coarse_bound, bound),
                              quadrature_signed=sup(prediction - np.array(case_rows[1]["budgets"][1]["signed_prediction"])),
                              quadrature_budget=relative(bound - np.array(case_rows[1]["budgets"][1]["combined_absolute_budget"]), bound))
            frozen_prediction = dict(model=model, branch=label, signed_prediction=prediction.tolist(), absolute_budget=bound.tolist(),
                                     refinement=refinement, cases=case_rows, reference_path=str(reference_path),
                                     reference_sha256=reference_row["sha256"], output_scales=output_scales.tolist(),
                                     no_target_history_input=True, numerically_certified_continuum_bound=False)
            write(RUN / "adjoints" / (model + "-" + label + "-frozen-prediction.json"), frozen_prediction)
            target_row = read(POISSON / "evolution" / (model + "-" + label + "-result.json"))
            require(digest(target_row["packet"]) == target_row["sha256"], "target readback")
            target = load(target_row["packet"])
            require(np.array_equal(grid, target["efold"]), "target grid")
            actual = (target["values"][-1, [value_names.index("D"), value_names.index("delta_c")]] - output_reference[-1]) / output_scales
            error = abs(prediction - actual)
            covers = abs(actual) <= bound
            passed = max(*refinement.values(), *error) < GATE and bool(np.all(covers))
            report = dict(model=model, branch=label, passed=bool(passed), prediction=prediction.tolist(), measured=actual.tolist(),
                          prediction_error=error.tolist(), absolute_budget=bound.tolist(), margin=(bound - abs(actual)).tolist(),
                          refinement=refinement, budget_covers_saved_output=covers.tolist(), target_sha256=target_row["sha256"],
                          cases=case_rows, continuum_certificate=False, terminal_only=True)
            write(RUN / "adjoints" / (model + "-" + label + "-result.json"), report)
            branch_rows.append(report)
            print(model, label, "comparison", {key: report[key] for key in ("prediction", "measured", "absolute_budget", "refinement", "passed")}, flush=True)
            require(passed, "inspect adjoint/budget discrepancy before next branch")
            del histories, target
        reports.append(dict(model=model, reports=branch_rows, numerical=numerical, algebra=split_errors))
        del operator, packet, system, context, core_reference, reference_spline
    check_parent()
    write(RUN / "adjoint-result.json", dict(passed=True, reports=reports, new_backward_solves=6, reused_backward_solves=2,
          reference_conditioned_terminal_bound=True, unknown_density_difference_input=False, rigorous_continuum_certificate=False))
    print("feedback adjoints and terminal budgets complete", flush=True)

if __name__ == "__main__":
    main()
