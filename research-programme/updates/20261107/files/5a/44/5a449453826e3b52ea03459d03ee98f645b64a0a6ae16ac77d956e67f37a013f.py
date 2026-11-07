from common import *
from primitive_math import *
from adjoint_operator import BRANCHES
from quadrature_v2 import integrate_budget, unit_checks
from scipy.interpolate import make_interp_spline
import sympy as sp


def symbolic():
    matrix = sp.Matrix(2, 2, sp.symbols("a0:4"))
    error = sp.Matrix(sp.symbols("e0:2"))
    direction = sp.Matrix(sp.symbols("d0:2"))
    direction_rate = sp.Matrix(sp.symbols("dn0:2"))
    force = sp.Matrix(sp.symbols("f0:2"))
    primitive, primitive_rate, source = sp.symbols("J Jn source")
    rate = matrix * error + force * source + direction * primitive_rate
    transformed_rate = rate - direction_rate * primitive - direction * primitive_rate
    expected = matrix * (error - direction * primitive) + force * source + (matrix * direction - direction_rate) * primitive
    return [str(sp.simplify(value)) for value in transformed_rate - expected]


def main():
    modest()
    check_parent()
    write(ROOT / "frozen-inputs.json", dict(sources={str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")},
          numerical=GATE, algebra=ALGEBRA, branches=BRANCHES, saved_caps=["cap", "half-cap"], new_ode_solves=0,
          bound_selection="report both, predeclared minimum only after all fixed precision gates"))
    identity = symbolic()
    require(all(value == "0" for value in identity), "source transformation")
    write(ROOT / "symbolic.json", identity)
    write(ROOT / "quadrature-tests.json", unit_checks())
    (ROOT / "contexts").mkdir(exist_ok=False)
    (ROOT / "results").mkdir(exist_ok=False)
    parent = read(ADJOINT / "response-v2/adjoint-result.json")
    build = read(ADJOINT / "build-result.json")
    reports = []
    for model in ("heavy", "cold"):
        guard()
        print(model, "loading retained coefficients and histories", flush=True)
        build_row = next(row for row in build["reports"] if row["model"] == model)
        require(digest(build_row["packet"]) == build_row["sha256"], "parent operator")
        coefficients = load(build_row["packet"])
        operator = CompactAdjoint(coefficients)
        model_parent = next(row for row in parent["reports"] if row["model"] == model)
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        reference_row = read(POISSON / "evolution" / (model + "-gr-result.json"))
        require(digest(reference_path) == reference_row["sha256"], "reference history")
        reference = load(reference_path)
        system = open_owned(model, "contexts")
        require(np.array_equal(system.units, coefficients["units"]), "fixed units")
        require(np.array_equal(reference["efold"], coefficients["efold"]), "original grid")
        grid = reference["efold"]
        physical_path = ADJOINT / "response-v2/adjoints" / (model + "-physical-sources.npz")
        physical = load(physical_path)
        primitive = MetricPrimitive(system, reference)
        sources, source_identity = primitive_sources(system, reference, physical)
        np.savez_compressed(ROOT / "results" / (model + "-primitive-sources.npz"), efold=grid, **sources)
        points = grid[np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))]
        indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
        points = grid[indices] + .43 * (grid[indices + 1] - grid[indices])
        numerical = {}
        keep = np.unique(np.r_[np.arange(0, len(grid), 2), len(grid) - 1])
        coarse = make_interp_spline(grid[keep], reference["diagnostics"][keep, 3], k=5)
        derivative_samples = {}
        for step in (1e-6, 5e-7):
            samples = {offset: np.array([primitive.direct_quadrature(float(efold + offset * step)) for efold in points]) for offset in (-2, -1, 1, 2)}
            derivative_samples[step] = (samples[-2] - 8 * samples[-1] + 8 * samples[1] - samples[2]) / (12 * step)
        scale = max(sup(derivative_samples[5e-7]), sup(primitive.quadrature(points)), 1e-80)
        numerical["quadrature_derivative_direct"] = sup(primitive.quadrature(points, 1) - derivative_samples[5e-7]) / scale
        numerical["quadrature_derivative_grid"] = sup(primitive.quadrature(points, 1) - coarse(points, 1)) / scale
        numerical["quadrature_derivative_step"] = sup(derivative_samples[1e-6] - derivative_samples[5e-7]) / scale
        primitive_curve = make_interp_spline(grid, sources["primitive"], k=5, axis=0)
        numerical["primitive_derivative"] = relative(primitive_curve(grid, 1) - sources["primitive_rate"], sources["primitive_rate"])
        branch_reports = []
        for branch, label in enumerate(BRANCHES):
            factor = 1. if branch == 0 else 0.
            vectors, vector_rates = [], []
            for efold in points:
                vector, rate, _ = primitive.vector(float(efold), factor)
                vectors.append(vector)
                vector_rates.append(rate)
            vectors, vector_rates = np.array(vectors), np.array(vector_rates)
            groups = dict(core=np.arange(operator.size))
            if model == "heavy":
                groups["heavy"] = system.slots
            finite = {}
            for step in (1e-6, 5e-7):
                samples = {offset: np.array([primitive.vector(float(efold + offset * step), factor, direct=True)[0] for efold in points]) for offset in (-2, -1, 1, 2)}
                finite[step] = (samples[-2] - 8 * samples[-1] + 8 * samples[1] - samples[2]) / (12 * step)
            for name, selection in groups.items():
                normal = max(sup(vector_rates[:, selection]), sup(vectors[:, selection]), 1e-80)
                numerical[label + "_full_derivative_" + name] = sup(vector_rates[:, selection] - finite[5e-7][:, selection]) / normal
                numerical[label + "_derivative_step_" + name] = sup(finite[1e-6][:, selection] - finite[5e-7][:, selection]) / normal
            direction = np.empty((len(grid), operator.size))
            direction_rate = np.empty_like(direction)
            commutator = np.empty_like(direction)
            tail_error, injection_error = 0., 0.
            for index, efold in enumerate(grid):
                if index % 256 == 0:
                    guard()
                direction[index], direction_rate[index], denominator = primitive.vector(float(efold), factor)
                full = np.zeros(operator.dimension)
                full[:operator.size] = direction[index]
                applied = operator.apply(float(efold), full, branch)
                commutator[index] = direction_rate[index] - applied[:operator.size]
                tail_error = max(tail_error, sup(applied[operator.size:]))
                expected = 3 * reference["H"][index] * coefficients["injection"][index, :, 1] / (system.wave * denominator)
                injection_error = max(injection_error, relative(direction[index] - expected, expected))
            require(tail_error == 0 and injection_error < ALGEBRA, "retained full-hierarchy injection")
            old_branch = next(row for row in model_parent["reports"] if row["branch"] == label)
            cases = []
            for old_case in old_branch["cases"]:
                require(digest(old_case["packet"]) == old_case["sha256"], "saved adjoint")
                saved = load(old_case["packet"])
                require(np.array_equal(grid, saved["efold"]), "saved output grid")
                dual = saved["adjoint_core"]
                response = np.einsum("nio,ni->no", dual, direction)
                response_rate = np.einsum("nio,ni->no", dual, commutator)
                adjoint_curve = make_interp_spline(grid, dual, k=5, axis=0)
                rate_from_curve, rate_from_operator = [], []
                for index, efold in enumerate(points):
                    state = adjoint_curve(float(efold))
                    state_rate = adjoint_curve(float(efold), 1)
                    rate_from_curve.append(np.einsum("io,i->o", state_rate, vectors[index]) + np.einsum("io,i->o", state, vector_rates[index]))
                    full = np.zeros(operator.dimension)
                    full[:operator.size] = vectors[index]
                    applied = operator.apply(float(efold), full, branch)[:operator.size]
                    rate_from_operator.append(np.einsum("io,i->o", state, vector_rates[index] - applied))
                for output, name in enumerate(("D", "delta_c")):
                    key = label + "_" + old_case["tag"] + "_contracted_derivative_" + name
                    numerical[key] = relative(np.array(rate_from_curve)[:, output] - np.array(rate_from_operator)[:, output], np.array(rate_from_operator)[:, output])
                boundary_terms = response[[0, -1]] * sources["primitive"][[0, -1], branch, None]
                boundary = boundary_terms[1] - boundary_terms[0]
                transformed = saved["physical_contributions"].copy()
                transformed[:, :, 2] = -response_rate * sources["primitive"][:, branch, None]
                integrals = [integrate_budget(grid, transformed, stride) for stride in (1, 2)]
                predictions = [boundary + np.array(item["signed_prediction"]) for item in integrals]
                bounds = [abs(boundary) + np.array(item["combined_absolute_budget"]) for item in integrals]
                temporal = boundary + np.array(integrals[0]["signed_channels"])[:, 2]
                temporal_bound = abs(boundary) + np.array(integrals[0]["channel_absolute_budgets"])[:, 2]
                old_temporal = np.array(old_case["physical_budgets"][0]["signed_channels"])[:, 2]
                replay = max(sup(predictions[0] - old_case["budgets"][0]["signed_prediction"]), sup(temporal - old_temporal))
                prefix = model + "-" + label + "-" + old_case["tag"]
                path = ROOT / "results" / (prefix + ".npz")
                np.savez_compressed(path, efold=grid, response=response, response_rate=response_rate, boundary_terms=boundary_terms,
                                    transformed=transformed, primitive=sources["primitive"][:, branch])
                case = dict(tag=old_case["tag"], packet=str(path), sha256=digest(path), original_adjoint=old_case["packet"],
                            original_adjoint_sha256=old_case["sha256"], prediction=predictions[0].tolist(), bound=bounds[0].tolist(),
                            boundary=boundary.tolist(), conservative_boundary=abs(boundary_terms).sum(axis=0).tolist(),
                            temporal_prediction=temporal.tolist(), temporal_bound=temporal_bound.tolist(),
                            original_temporal_budget=old_case["physical_budgets"][0]["channel_absolute_budgets"],
                            replay_error=replay, integrals=integrals,
                            quadrature_signed=sup(predictions[0] - predictions[1]), quadrature_budget=relative(bounds[0] - bounds[1], bounds[0]))
                write(ROOT / "results" / (prefix + "-prediction.json"), case)
                cases.append(case)
                print(prefix, "prediction", case["prediction"], "bound", case["bound"], "replay", replay, flush=True)
                require(max(replay, case["quadrature_signed"], case["quadrature_budget"]) < GATE, "primitive reconstruction/integration")
            step = dict(prediction=sup(np.array(cases[0]["prediction"]) - cases[1]["prediction"]),
                        budget=relative(np.array(cases[0]["bound"]) - cases[1]["bound"], cases[1]["bound"]))
            measured = np.array(old_branch["measured"])
            prediction = np.array(cases[1]["prediction"])
            bound = np.array(cases[1]["bound"])
            old_bound = np.array(old_branch["absolute_budget"])
            result = dict(model=model, branch=label, cases=cases, step_refinement=step, prediction=prediction.tolist(),
                          measured=measured.tolist(), prediction_error=abs(prediction - measured).tolist(), transformed_bound=bound.tolist(),
                          old_bound=old_bound.tolist(), selected_bound=np.minimum(bound, old_bound).tolist(),
                          improvement_factor=(old_bound / bound).tolist(), tail_injection=tail_error, injection_identity=injection_error,
                          passed=bool(max(*step.values(), sup(prediction - measured)) < GATE and np.all(abs(measured) <= bound)))
            write(ROOT / "results" / (model + "-" + label + "-result.json"), result)
            branch_reports.append(result)
            require(result["passed"], "inspect primitive comparison")
            del direction, direction_rate, commutator
        passed = all(value < GATE for value in numerical.values())
        model_report = dict(model=model, numerical=numerical, algebra=source_identity, branches=branch_reports, passed=passed)
        write(ROOT / "results" / (model + "-result.json"), model_report)
        print(model, "derivative checks", numerical, "passed", passed, flush=True)
        reports.append(model_report)
        require(passed, "inspect full derivative qualification")
        del operator, coefficients, system, reference
    check_parent()
    write(ROOT / "primitive-result.json", dict(passed=True, reports=reports, new_ode_solves=0,
          exact_primitive_from_GR_constraint=True, slow_adjoint_assumed=False, new_physical_parameters=False,
          rigorous_continuum_certificate=False, terminal_only=True))
    print("metric-time primitive response complete", flush=True)

if __name__ == "__main__":
    main()

