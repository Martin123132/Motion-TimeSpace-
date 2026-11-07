from common import *
from polynomial_budget import scaled_power, multiply, signed_integral, absolute_integral, supremum_upper, unit_checks
from phase_probe import symbolic_checks, native_phase_probe
import numpy as np


def sup(value):
    return float(np.max(abs(np.asarray(value))))


def relative(value, scale):
    return sup(value) / max(sup(scale), 1e-80)


def analyze(grid, gain, response, response_rate, sources, stride):
    keep = np.unique(np.r_[np.arange(0, len(grid), stride), len(grid) - 1])
    selected = grid[keep]
    kernels = np.stack([gain + response_rate, gain], axis=2)
    kernel_power = scaled_power(selected, kernels[keep])
    source_power = scaled_power(selected, sources[keep])
    product = multiply(kernel_power, source_power[:, None, :, :])
    channel_signed = signed_integral(selected, product)
    boundary_terms = -response[[0, -1]] * sources[[0, -1], 0, None]
    boundary = boundary_terms[1] - boundary_terms[0]
    boundary_absolute = abs(boundary_terms).sum(axis=0)
    kernel_norm, _, kernel_gap = absolute_integral(selected, kernel_power)
    separate_power = scaled_power(selected, np.stack([gain, response_rate], axis=2)[keep])
    separate_norm, _, separate_gap = absolute_integral(selected, separate_power)
    channel_upper, channel_lower, channel_gap = absolute_integral(selected, product)
    combined_upper, combined_lower, combined_gap = absolute_integral(selected, product.sum(axis=2))
    source_sup = supremum_upper(source_power)
    endpoint_gain = abs(response[[0, -1]]).sum(axis=0)
    holder_terms = np.stack([endpoint_gain * source_sup[0], kernel_norm[:, 0] * source_sup[0], kernel_norm[:, 1] * source_sup[1]], axis=1)
    holder = holder_terms.sum(axis=1)
    triangle = boundary_absolute + channel_upper.sum(axis=1)
    combined = abs(boundary) + combined_upper
    prediction = boundary + channel_signed.sum(axis=1)
    scale = max(sup(holder), 1e-80)
    require(np.all(combined <= triangle + ALGEBRA * scale) and np.all(triangle <= holder + ALGEBRA * scale), "polynomial Holder hierarchy")
    require(np.all(abs(prediction) <= combined + ALGEBRA * scale), "polynomial absolute bound")
    return dict(stride=stride, prediction=prediction.tolist(), boundary=boundary.tolist(),
                boundary_absolute=boundary_absolute.tolist(), channel_signed=channel_signed.tolist(),
                combined_budget=combined.tolist(), triangle_budget=triangle.tolist(), holder_budget=holder.tolist(),
                holder_terms=holder_terms.tolist(), source_suprema=source_sup.tolist(), kernel_L1=kernel_norm.tolist(),
                endpoint_gain=endpoint_gain.tolist(), separate_G_CN_L1=separate_norm.tolist(),
                cancellation_factor=(separate_norm.sum(axis=1) / np.maximum(kernel_norm[:, 0], 1e-80)).tolist(),
                channel_upper=channel_upper.tolist(), channel_lower=channel_lower.tolist(),
                maximum_enclosure_gap=max(kernel_gap, separate_gap, channel_gap, combined_gap),
                exact_product_degree=6, sampled_source_max_used_as_envelope=False)


def main():
    modest()
    check_parent()
    require(LABEL != "summary", "explicit numerical family")
    ROOT.mkdir(exist_ok=True)
    write(ROOT / "inputs.json", dict(sources=frozen_sources(), wave=WAVE, algebra=ALGEBRA, numerical=GATE,
          old_bank_grids_tolerances=True, new_ode_solves=0, prospective_claim="conditional source-gain bound, not uniform convergence proof",
          pairwise_products="exact degree-six product of separate saved cubic reconstructions"))
    write(ROOT / "polynomial-tests.json", unit_checks())
    write(ROOT / "symbolic-phase.json", symbolic_checks())
    checks = []
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
    parent_result = read(PRIMITIVE / "primitive-result.json")
    models = []
    inputs = {}
    for model in ("heavy", "cold"):
        guard()
        physical_path = ADJOINT / "response-v2/adjoints" / (model + "-physical-sources.npz")
        physical = load(physical_path)
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        reference = load(reference_path)
        inputs[str(physical_path)] = digest(physical_path)
        inputs[str(reference_path)] = digest(reference_path)
        grid = physical["efold"]
        require(np.array_equal(grid, reference["efold"]), "fixed reference grid")
        require(float(reference["wave"]) == WAVE, "actual wavenumber")
        sources = np.column_stack([physical["momentum"], physical["shear"]])
        old_model = next(item for item in parent_result["reports"] if item["model"] == model)
        old_branch = next(item for item in old_model["branches"] if item["branch"] == "poisson-spatial")
        cases = []
        for old_case in old_branch["cases"]:
            guard()
            primitive_path = Path(old_case["packet"])
            adjoint_path = Path(old_case["original_adjoint"])
            require(digest(primitive_path) == old_case["sha256"] and digest(adjoint_path) == old_case["original_adjoint_sha256"], "saved input hash")
            inputs[str(primitive_path)] = digest(primitive_path)
            inputs[str(adjoint_path)] = digest(adjoint_path)
            primitive = load(primitive_path)
            saved = load(adjoint_path)
            require(np.array_equal(grid, primitive["efold"]) and np.array_equal(grid, saved["efold"]), "saved common grid")
            gain = saved["gain_channels"][:, :, 0]
            response, response_rate = primitive["response"], primitive["response_rate"]
            merged = (gain + response_rate) * sources[:, 0, None] + gain * sources[:, 1, None]
            prefix = model + ":" + old_case["tag"]
            check(prefix + ":J=-M", relative(primitive["primitive"] + sources[:, 0], sources[:, 0]) < ALGEBRA)
            reconstruction = relative(merged - primitive["transformed"].sum(axis=2), primitive["transformed"])
            check(prefix + ":source-reconstruction", reconstruction < ALGEBRA, reconstruction)
            budgets = [analyze(grid, gain, response, response_rate, sources, stride) for stride in (1, 2)]
            for name in ("source_suprema", "kernel_L1", "holder_budget", "combined_budget"):
                error = relative(np.array(budgets[0][name]) - budgets[1][name], budgets[0][name])
                check(prefix + ":grid:" + name, error < GATE, error)
            replay = sup(np.array(budgets[0]["prediction"]) - old_case["prediction"])
            check(prefix + ":product-versus-saved-cubic", replay < GATE, replay)
            measured = np.array(old_branch["measured"])
            readback = sup(np.array(budgets[0]["prediction"]) - measured)
            check(prefix + ":independent-readback", readback < GATE, readback)
            check(prefix + ":holder-covers", np.all(abs(measured) <= np.array(budgets[0]["holder_budget"])))
            check(prefix + ":combined-covers", np.all(abs(measured) <= np.array(budgets[0]["combined_budget"])))
            packet_path = ROOT / (model + "-" + old_case["tag"] + "-kernels.npz")
            np.savez_compressed(packet_path, efold=grid, sources=sources, gain=gain, response=response,
                                response_rate=response_rate, current_kernel=gain + response_rate)
            case = dict(tag=old_case["tag"], budgets=budgets, packet=str(packet_path), sha256=digest(packet_path),
                        replay_error=replay, readback_error=readback)
            write(ROOT / (model + "-" + old_case["tag"] + ".json"), case)
            cases.append(case)
            del saved, primitive
        for name in ("source_suprema", "kernel_L1", "holder_budget", "combined_budget"):
            error = relative(np.array(cases[0]["budgets"][0][name]) - cases[1]["budgets"][0][name], cases[1]["budgets"][0][name])
            check(model + ":adjoint-step:" + name, error < GATE, error)
        names = reference["value_names"].tolist()
        current = reference["values"][:, names.index("Q")]
        shear = reference["values"][:, names.index("Pi")]
        physical_identity = dict(current=relative(sources[:, 0] - 1.5 * (reference["H"] / WAVE) * (current / WAVE**2), sources[:, 0]),
                                 shear=relative(sources[:, 1] - shear / WAVE**2, sources[:, 1]))
        for name, value in physical_identity.items():
            check(model + ":physical-source:" + name, value < ALGEBRA, value)
        models.append(dict(model=model, wave=WAVE, measured=old_branch["measured"],
                           retained_raw_bound=old_branch["old_bound"], retained_primitive_bound=old_branch["transformed_bound"],
                           physical=physical_identity, H_over_k_sample_max=sup(reference["H"] / WAVE),
                           N_interval=[float(grid[0]), float(grid[-1])], cases=cases))
        print(LABEL, model, "fine Holder", cases[1]["budgets"][0]["holder_budget"], "source suprema", cases[1]["budgets"][0]["source_suprema"], flush=True)
    phase = native_phase_probe()
    check("native-heavy-phase-cancellation", phase["passed"], phase["errors"])
    for path, expected in read(ROOT / "inputs.json")["sources"].items():
        check("frozen:" + path, digest(path) == expected)
    for path, expected in inputs.items():
        check("reused:" + path, digest(path) == expected)
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "result.json", dict(passed=passed, reports=models, phase=phase["errors"], input_hashes=inputs,
                                    new_ode_solves=0, original_cases_reused=4, wave=WAVE))
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks))
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    print(LABEL, "checks", len(checks), "passed", passed, flush=True)
    require(passed, "preserve and inspect source-gain gate")


if __name__ == "__main__":
    main()

