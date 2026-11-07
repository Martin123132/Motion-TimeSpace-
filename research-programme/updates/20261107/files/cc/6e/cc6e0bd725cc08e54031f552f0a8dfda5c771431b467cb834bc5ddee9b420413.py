from common import *
from corrector_v2 import *
from coefficients import calculate
from canonical_math import transform
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT / "assembly-result.json")["passed"], "assembly")
    sources = {str(STAGE / name): digest(STAGE / name) for name in ("common.py", "corrector.py", "corrector_v2.py", "channel_probe.py", "run_probe.ps1")}
    write(ROOT / "channel-inputs.json", dict(sources=sources, numerical=GATE, algebra=ALGEBRA))
    context, system, units, support, vectors, wave = initialize("channel-contexts")
    provider = Background("heavy")
    indices = np.unique(np.linspace(1, len(provider.efold) - 3, 33, dtype=int))
    points = provider.efold[indices] + .37 * (provider.efold[indices + 1] - provider.efold[indices])
    data = factors(provider, system, support, points, wave)
    coefficients = calculate(provider, points, wave)
    exact = transform(provider.evaluate(points), wave, include_fast=False)
    random = np.random.default_rng(7082026)
    checks = {}
    for index, efold in enumerate(points):
        guard()
        ub = tuple(data["V_" + suffix][index] for suffix in ("A", "B", "C"))
        balance = exact["balance"][index]
        matrix = coefficients["transform"][index]
        matrix_rate = exact["rate"][index] * balance[:, None] / balance[None, :]
        for direction in ("canonical-only", "source-only", "combined"):
            vector = random.normal(size=len(units)) * units
            if direction == "canonical-only":
                vector[8:] = 0.
            elif direction == "source-only":
                vector[:8] = 0.
                rest = np.zeros(system.rest_size)
                rest[support] = vector[8:][support]
                vector[8:] = rest
            internal, linear, _, _ = system.source_only(float(efold), vector[8:])
            mean_state = JFULL @ (coefficients["hessian"][index] @ vector[:8] + coefficients["source"][index] @ linear)
            mean_native = internal + vectors[:system.native_rest_size] @ (coefficients["feedback"][index] @ vector[:8]) / context["point"](float(efold))[12]
            approximation = np.r_[mean_state, system.extend_tail(float(efold), vector[8:], mean_native)] + apply(ub, vector, support, vectors)
            state_rate, rest_rate = system.full_rhs(float(efold), matrix @ vector[:8], vector[8:])
            original = np.r_[np.linalg.solve(matrix, state_rate - matrix_rate @ vector[:8]), rest_rate]
            for channel, selection in (("canonical", slice(0, 8)), ("rest", slice(8, None))):
                scale_value = max(np.max(abs(original[selection] / units[selection])), 1e-80)
                value = float(np.max(abs((approximation[selection] - original[selection]) / units[selection])) / scale_value)
                name = direction + ":" + channel
                checks[name] = max(checks.get(name, 0.), value)
    passed = all(np.isfinite(value) and value < GATE for value in checks.values())
    write(ROOT / "channel-result.json", dict(passed=bool(passed), checks=checks, probes=len(points),
          numerical=GATE, label=LABEL, normalization="separate canonical/rest, source-only and canonical-only directions"))
    print("Separated native operator channels", LABEL, checks, "passed", passed, flush=True)
    require(passed, "channel test failed; inspect before forward")


if __name__ == "__main__":
    main()

