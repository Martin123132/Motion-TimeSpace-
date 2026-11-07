from common import ROOT, SECOND, ALGEBRA, GATE, modest, guard, check_parent, require, write, read, digest
from canonical_math import Background, coefficients, generator, transform, physical_matrix, joint_extractor, JFULL, transpose, sup, norm
import numpy as np


def balanced(matrix, units):
    return matrix * units[:, None, :] / units[:, :, None]


def evaluate(background, points, wave):
    guard()
    return transform(background.evaluate(points), wave, include_fast=False)


def main():
    modest()
    check_parent()
    sources = {str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".md", ".ps1")}
    write(ROOT / "frozen-inputs.json", dict(sources=sources, algebra=ALGEBRA, numerical=GATE))
    background = Background("heavy")
    grid = background.efold
    probes = np.linspace(grid[0] + .013 * (grid[-1] - grid[0]), grid[-1] - .017 * (grid[-1] - grid[0]), 97)
    model = background.evaluate(probes)
    node_model = background.evaluate(grid)
    base = background.packet
    node_checks = dict(
        hubble=sup(node_model["hubble"] - base["H"]) / norm(base["H"]),
        carrier=sup(node_model["mu"] - base["a"] * base["masses"][1] / base["H"]) / norm(node_model["mu"]),
        velocity_s=sup(node_model["velocity_s"] - base["velocities"][:, 0]) / norm(base["velocities"][:, 0]))
    coarse = background.evaluate(probes, coarse=True)
    coarse_checks = {name: sup(model[name] - coarse[name]) / norm(model[name]) for name in ("hubble", "hlog", "background", "background_rate")}
    direct = joint_extractor()[1]
    rows = []
    owner = read(SECOND / "prediction-result.json")
    for family in owner["reports"]:
        if family["model"] != "heavy":
            continue
        guard()
        wave = family["wave"]
        result = evaluate(background, probes, wave)
        units = result["balance"]
        analytic_hessian, generating, derivative, fast = generator(model, wave)
        parent_hessian = direct(model["scale"], model["hubble"], model["omega_s"], model["velocity_s"], model["omega_h"],
                                model["background"], model["mu"], model["phase"], wave)[0]
        hscale = units[:, :, None] * units[:, None, :]
        algebra = dict(
            original_hamiltonian=sup((analytic_hessian - parent_hessian) * hscale) / norm(parent_hessian * hscale),
            symplectic=sup(transpose(result["transform"]) @ JFULL @ result["transform"] - JFULL),
            inverse=sup((-JFULL @ transpose(result["transform"]) @ JFULL) @ result["transform"] - np.eye(8)))
        values, rates = coefficients(model, wave)
        derivatives = []
        for step in (1e-6, 5e-7):
            shifted = [background.evaluate(probes + offset * step) for offset in (-2, -1, 1, 2)]
            shifted_coefficients = [coefficients(item, wave)[0] for item in shifted]
            numeric_coefficients = (shifted_coefficients[0] - 8 * shifted_coefficients[1] + 8 * shifted_coefficients[2] - shifted_coefficients[3]) / (12 * step)
            coefficient_error = sup((numeric_coefficients - rates) * hscale[:, None]) / norm(rates * hscale[:, None])
            shifted_generator = [generator(item, wave)[1] for item in shifted]
            numeric_generator = (shifted_generator[0] - 8 * shifted_generator[1] + 8 * shifted_generator[2] - shifted_generator[3]) / (12 * step)
            generator_error = sup(balanced(JFULL @ (numeric_generator - derivative), units)) / norm(balanced(JFULL @ derivative, units))
            shifted_transform = [transform(item, wave, include_fast=False) for item in shifted]
            physical = [physical_matrix(item["transform"], item["balance"]) for item in shifted_transform]
            numeric_transform = (physical[0] - 8 * physical[1] + 8 * physical[2] - physical[3]) / (12 * step)
            transform_error = sup(balanced(numeric_transform, units) - result["rate"]) / norm(result["rate"])
            derivatives.append(dict(step=step, coefficients=coefficient_error, generator=generator_error, transform=transform_error))
        coarse_result = transform(coarse, wave, include_fast=False)
        coarse_error = sup(balanced(physical_matrix(coarse_result["rate"], coarse_result["balance"]), units) - result["rate"]) / norm(result["rate"])
        row = dict(label=family["label"], wave=wave, algebra=algebra, derivative_checks=derivatives,
                   rest_density_refinement_rate_error=coarse_error,
                   coefficient_derivative_omission_fraction=sup(balanced(JFULL @ (derivative - fast), units)) / norm(balanced(JFULL @ derivative, units)))
        row["passed"] = max(algebra.values()) < ALGEBRA and max(max(item[name] for name in ("coefficients", "generator", "transform")) for item in derivatives) < GATE and coarse_error < GATE
        rows.append(row)
        print(row, flush=True)
    passed = max(node_checks.values()) < ALGEBRA and max(coarse_checks.values()) < GATE and all(row["passed"] for row in rows)
    write(ROOT / "probe-result.json", dict(passed=passed, probes=len(probes), node_checks=node_checks, background_interpolation_checks=coarse_checks, rows=rows))
    require(passed, "independent derivative checks failed; preserve and inspect")
    print("Independent actual-background derivative checks passed", flush=True)


if __name__ == "__main__":
    main()
