import math
from common import ROOT, modest, guard, check_parent, require, read, write, digest, ALGEBRA
from mean_math import *
import numpy as np


def frobenius(value):
    return np.linalg.norm(value, axis=(-2, -1))


def envelope(polynomial):
    return sum(frobenius(value) for value in polynomial.values())


def main():
    modest()
    check_parent()
    result = read(ROOT / "result.json")
    require(result["passed"], "mean qualification")
    provider = Background("heavy")
    reports = []
    for family in result["families"]:
        guard()
        require(digest(family["profile"]) == family["sha256"], "profile integrity")
        packet = load(family["profile"])
        original, mean, cosine, sine = phase_background(provider, packet["points"])
        hessian, exponent, exponent_rate, units = polynomials(mean, cosine, sine, family["wave"])
        constraint = constraint_polynomial(mean, family["wave"], units)
        radius, hessian_size, derivative_size, constraint_size = [envelope(item) for item in (exponent, hessian, exponent_rate, constraint)]
        order = 2
        connection_bound = derivative_size * np.exp(2 * radius) * (2 * radius)**(order + 1) / math.factorial(order + 2)
        conjugation_bound = hessian_size * np.exp(2 * radius) * (2 * radius)**(order + 1) / math.factorial(order + 1)
        action_bound = connection_bound + conjugation_bound
        map_bound = np.exp(radius) * radius**(order + 1) / math.factorial(order + 1)
        constraint_bound = constraint_size * map_bound
        errors = dict(hessian=frobenius(packet["mean_hessian"] - packet["exact_mean_hessian"]),
                      source=frobenius(packet["mean_source"] - packet["exact_mean_source"]),
                      constraint=frobenius(packet["mean_constraint"] - packet["exact_mean_constraint"]))
        bounds = dict(hessian=action_bound, source=map_bound, constraint=constraint_bound)
        references = dict(hessian=frobenius(packet["exact_mean_hessian"]), source=frobenius(packet["exact_mean_source"]),
                          constraint=frobenius(packet["exact_mean_constraint"]))
        checks = {name: bool(np.all(error <= bounds[name] + ALGEBRA * np.maximum(references[name], 1e-80))) for name, error in errors.items()}
        report = dict(family=family["family"], phase_uniform=True, sampled_times=len(radius), order=order,
                      maximum_exponent_norm_bound=float(np.max(radius)), checks=checks, passed=all(checks.values()),
                      relative_bounds={name: float(np.max(value / np.maximum(references[name], 1e-80))) for name, value in bounds.items()},
                      mean_error_over_analytic_bound={name: float(np.max(errors[name] / np.maximum(value, 1e-80))) for name, value in bounds.items()},
                      arithmetic_scope="analytic norm inequality; ordinary floating-point evaluation, not interval-certified numerics")
        output = ROOT / "profiles" / (family["family"] + "-remainder-bounds.npz")
        np.savez_compressed(output, points=packet["points"], exponent_bound=radius, hessian_bound=action_bound,
                            source_bound=map_bound, constraint_bound=constraint_bound, **{name + "_error": value for name, value in errors.items()})
        report["profile"] = str(output)
        report["sha256"] = digest(output)
        reports.append(report)
        print(report, flush=True)
    check_parent()
    passed = all(row["passed"] for row in reports)
    write(ROOT / "remainder-bounds.json", dict(passed=passed, order=2, reports=reports,
          source_hashes={str(ROOT / name): digest(ROOT / name) for name in ("bound_remainder.py", "mean_math.py", "common.py", "result.json")}))
    require(passed, "bound diagnostic failed; inspect")


if __name__ == "__main__":
    main()
