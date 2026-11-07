from common import *
from coefficient_loader import coefficients as original_coefficients
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative
from energy_map import EnergyMap
import numpy as np


def coefficients(model):
    cached = ROOT / (model + "-central-packing.json")
    if LABEL == "balanced" and cached.exists():
        receipt = read(cached)
        require(digest(receipt["packet"]) == receipt["sha256"], "retained exact central packing")
        require(digest(receipt["input"]) == receipt["input_sha256"], "central packing source")
        return load(receipt["packet"])
    return original_coefficients(model)


def main():
    modest()
    check_parent()
    ROOT.mkdir(exist_ok=True)
    write(ROOT / "probe-v2-inputs.json", dict(sources=frozen_sources(), wave=WAVE, new_ode_solves=0, algebra=ALGEBRA, numerical=GATE))
    (ROOT / "probe-contexts-v2").mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        packet = coefficients(model)
        operator = CompactAdjoint(packet)
        system = open_owned(model, "probe-contexts-v2")
        require(np.array_equal(packet["units"], system.units), "native normalization")
        energy = EnergyMap(system)
        grid = packet["efold"]
        indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
        rows = []
        maximum_skew, maximum_roundtrip = 0., 0.
        for index in indices:
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            core = operator.blocks(efold, 0)[0]
            matrix, transform, inverse, condition = energy.generator(efold, core)
            comparison = energy.comparison(matrix)
            roundtrip = relative(transform @ inverse - np.eye(len(core)), np.eye(len(core)))
            maximum_roundtrip = max(maximum_roundtrip, roundtrip)
            maximum_skew = max(maximum_skew, energy.hierarchy_skew(operator, efold))
            rate = float(np.linalg.eigvalsh((matrix + matrix.T) / 2)[-1])
            rows.append(dict(efold=efold, comparison=comparison.tolist(), whole_core_rate=rate, heavy_condition=condition))
        maximum = np.max(np.array([row["comparison"] for row in rows]), axis=0)
        span = float(grid[-1] - grid[0])
        radius = float(np.linalg.eigvals(maximum).real.max())
        owner = next(item for item in read(PRIMITIVE / "primitive-result.json")["reports"] if item["model"] == model)
        branch = next(item for item in owner["branches"] if item["branch"] == "poisson-spatial")
        record = next(item for item in branch["cases"] if item["tag"] == "half-cap")
        require(digest(record["original_adjoint"]) == record["original_adjoint_sha256"], "owner-recorded adjoint")
        saved = load(record["original_adjoint"])
        output_scales = saved["output_scales"]
        gain_result = read(LATEST / LABEL / "result.json")
        gain = next(item for item in gain_result["reports"] if item["model"] == model)["cases"][1]["budgets"][0]
        raw_kernel = np.array(gain["kernel_L1"]) * output_scales[:, None]
        report = dict(model=model, rows=rows, sampled_max_comparison=maximum.tolist(), interval_span=span,
                      sampled_constant_log_growth=span * radius, maximum_hierarchy_skew=maximum_skew,
                      maximum_transform_roundtrip=maximum_roundtrip, output_scales=output_scales.tolist(),
                      raw_kernel_L1=raw_kernel.tolist(), normalized_kernel_L1=gain["kernel_L1"],
                      sampled_envelope_only=True, new_ode_solves=0,
                      passed=maximum_skew < ALGEBRA and maximum_roundtrip < ALGEBRA)
        write(ROOT / (model + "-probe.json"), report)
        print(LABEL, model, "comparison", maximum.tolist(), "sampled log gain", span * radius, "raw kernels", raw_kernel.tolist(), flush=True)
        require(report["passed"], "energy map probe")
        reports.append(report)
        del operator, packet, system
    for path, expected in read(ROOT / "probe-v2-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen probe source")
    check_parent()
    write(ROOT / "probe-result.json", dict(passed=True, reports=reports, sampled_envelope_only=True))


if __name__ == "__main__":
    main()
