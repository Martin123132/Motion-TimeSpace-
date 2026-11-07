from common import *
from coefficient_loader import coefficients
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative
from physical_energy_map import PhysicalEnergyMap
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT / "probe-result.json")["passed"], "inspected original norm")
    write(ROOT / "physical-inputs.json", dict(sources=frozen_sources(), algebra=ALGEBRA, numerical=GATE,
          no_fit=True, no_new_ode=True, observational_readouts_unchanged=True))
    (ROOT / "physical-contexts").mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        if LABEL == "balanced":
            packed = read(ROOT / (model + "-central-packing.json"))
            require(digest(packed["packet"]) == packed["sha256"], "lossless existing central coefficients")
            packet = load(packed["packet"])
        else:
            packet = coefficients(model)
        operator = CompactAdjoint(packet)
        system = open_owned(model, "physical-contexts")
        energy = PhysicalEnergyMap(system)
        grid = packet["efold"]
        indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
        rows = []
        errors = dict(roundtrip=0., hierarchy_skew=0., derivative=0., derivative_step=0., native_rhs=0.)
        for count, index in enumerate(indices):
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            core = operator.blocks(efold, 0)[0]
            matrix, transform, inverse, conditions = energy.generator(efold, core)
            comparison = energy.comparison(matrix)
            errors["roundtrip"] = max(errors["roundtrip"], relative(transform @ inverse - np.eye(len(core)), np.eye(len(core))))
            errors["hierarchy_skew"] = max(errors["hierarchy_skew"], energy.hierarchy_skew(operator, efold))
            if count % 8 == 0:
                derivative = energy.blocks(efold)[2] @ transform
                approximations = {}
                for step in (1e-6, 5e-7):
                    samples = {offset: energy.blocks(efold + offset * step)[0] for offset in (-2, -1, 1, 2)}
                    approximations[step] = (samples[-2] - 8 * samples[-1] + 8 * samples[1] - samples[2]) / (12 * step)
                errors["derivative"] = max(errors["derivative"], relative(derivative - approximations[5e-7], derivative))
                errors["derivative_step"] = max(errors["derivative_step"], relative(approximations[1e-6] - approximations[5e-7], derivative))
                vector = np.sin(np.arange(len(system.units)) + count + .3)
                direct = system.evaluate(efold, vector * system.units, "poisson-spatial")[0] / system.units
                interpolated = operator.apply(efold, vector, 0)
                errors["native_rhs"] = max(errors["native_rhs"], relative(transform @ (direct[:operator.size] - interpolated[:operator.size]), transform @ direct[:operator.size]))
            rows.append(dict(efold=efold, comparison=comparison.tolist(), conditions=conditions))
        maximum = np.max(np.array([row["comparison"] for row in rows]), axis=0)
        rate = float(np.linalg.eigvals(maximum).real.max())
        passed = errors["roundtrip"] < ALGEBRA and errors["hierarchy_skew"] < ALGEBRA and max(errors["derivative"], errors["derivative_step"], errors["native_rhs"]) < GATE
        report = dict(model=model, passed=bool(passed), errors=errors, rows=rows,
                      sampled_max_comparison=maximum.tolist(), sampled_constant_log_gain=rate * float(grid[-1] - grid[0]),
                      physical_energy_map=True, original_data_and_model_unchanged=True, sampled_not_interval_certificate=True)
        write(ROOT / (model + "-physical-probe.json"), report)
        print(LABEL, model, "physical comparison", maximum.tolist(), "sample log gain", report["sampled_constant_log_gain"], "errors", errors, flush=True)
        require(passed, "inspect physical norm gate")
        reports.append(report)
        del operator, packet, system
    for path, expected in read(ROOT / "physical-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen physical source")
    check_parent()
    write(ROOT / "physical-probe-result.json", dict(passed=True, reports=reports))


if __name__ == "__main__":
    main()

