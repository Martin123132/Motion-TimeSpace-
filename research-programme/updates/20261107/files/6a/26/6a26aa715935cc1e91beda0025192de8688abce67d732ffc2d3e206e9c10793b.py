from common import *
from corrector_v2 import *
import numpy as np


def main():
    modest()
    check_parent()
    original = read(ROOT / "assembly-result.json")
    require(not original["passed"], "preserve initial failed representation")
    failed = {name for name, value in original["checks"].items() if value >= GATE}
    require(failed == {"grid_derivative_U_A", "grid_derivative_U_B", "grid_derivative_U_C"}, "inspect unexpected earlier failure")
    require(digest(ROOT / "coupled-factors.npz") == original["packet_sha256"], "reuse factor packet")
    sources = {str(path): digest(path) for path in ROOT.iterdir() if path.suffix in (".py", ".ps1", ".md")}
    sources.update({str(ROOT / name): digest(ROOT / name) for name in ("assembly-result.json", "coupled-factors.npz", "representation-checks.npz")})
    write(ROOT / "representation-v2-inputs.json", dict(sources=sources, numerical=GATE, algebra=ALGEBRA,
                                                     original_grid_preserved=True, interpolation_order=5))
    packet = load(ROOT / "coupled-factors.npz")
    reference = load(ROOT / "representation-checks.npz")
    context, system, units, support, vectors, wave = initialize("contexts-v2")
    require(np.array_equal(units, packet["units"]) and np.array_equal(support, packet["support"]) and np.array_equal(vectors, packet["vectors"]), "native seed representation")
    mapping = HigherOrderCorrector(packet)
    points = reference["points"]
    direct = factors(Background("heavy"), system, support, points, wave)
    checks = {}
    keep = np.unique(np.r_[np.arange(0, len(packet["efold"]), 2), len(packet["efold"]) - 1])
    for name in mapping.splines:
        denominator = max(np.max(abs(balanced_block(direct[name], name, units, support, vectors))), 1e-80)
        checks["value_" + name] = float(np.max(abs(balanced_block(mapping.splines[name](points) - direct[name], name, units, support, vectors))) / denominator)
        if name.startswith("U"):
            fine = mapping.splines[name](points, 1)
            coarse = make_interp_spline(packet["efold"][keep], packet[name][keep], k=5, axis=0)(points, 1)
            derivative = reference["derivative_" + name]
            denominator = max(np.max(abs(balanced_block(derivative, name, units, support, vectors))), 1e-80)
            checks["derivative_" + name] = float(np.max(abs(balanced_block(fine - derivative, name, units, support, vectors))) / denominator)
            checks["grid_derivative_" + name] = float(np.max(abs(balanced_block(fine - coarse, name, units, support, vectors))) / denominator)
            checks["fd_refinement_" + name] = original["checks"]["fd_refinement_" + name]
    checks["order2_full_operator"] = original["checks"]["order2_full_operator"]
    sampled_norms = [infinity_norm(mapping.blocks(float(efold)), units, support, vectors) for efold in points]
    maximum = max(original["maximum_native_normalized_U"], max(sampled_norms))
    passed = all(np.isfinite(value) and value < GATE for value in checks.values()) and maximum < 1
    write(ROOT / "representation-v2-result.json", dict(passed=bool(passed), checks=checks, algebra=original["algebra"],
          maximum_sampled_U=float(maximum), sampled_inverse_bound=float(1 / (1 - maximum)),
          original_points=original["points"], independent_probes=len(points), interpolation_order=5,
          packet_sha256=original["packet_sha256"], grid_changed=False, original_failure_preserved=True,
          numerical=GATE, continuous_time_certificate=False))
    print("Quintic same-node checks", checks, "U bound", maximum, "passed", passed, flush=True)
    require(passed, "quintic representation failed; inspect")


if __name__ == "__main__":
    main()

