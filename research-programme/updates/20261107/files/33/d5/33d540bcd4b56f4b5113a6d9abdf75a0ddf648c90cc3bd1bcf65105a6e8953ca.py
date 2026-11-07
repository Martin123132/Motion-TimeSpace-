from common import *
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from primitive_math import MetricPrimitive
from comparison_math import propagate, unit_checks
from scipy.interpolate import make_interp_spline
import numpy as np


def main():
    modest()
    check_parent()
    result = read(ROOT / "bound/result.json")
    require(result["passed"], "closed bound result")
    checks = []
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
    (ROOT / "verification-contexts").mkdir(exist_ok=False)
    check("polynomial-and-affine-reference", unit_checks()["passed"])
    for source, expected in read(ROOT / "bound/inputs.json")["sources"].items():
        check("frozen:" + source, digest(source) == expected)
    for report in result["reports"]:
        model = report["model"]
        check(model + ":packet-hash", digest(report["packet"]) == report["sha256"])
        for chunk in report["chunks"]:
            check(model + ":chunk:" + str(chunk["begin"]), digest(chunk["path"]) == chunk["sha256"])
        saved = load(report["packet"])
        grid = saved["efold"]
        system = open_owned(model, "verification-contexts")
        energy = PhysicalEnergyMap(system)
        size = len(system.core)
        core_curve = make_interp_spline(grid, saved["core"], k=5, axis=0)
        source_curve = make_interp_spline(grid, saved["source"], k=5, axis=0)
        maximum_excess = 0.
        for index in np.unique(np.linspace(0, len(grid) - 2, 97, dtype=int)):
            for fraction in (.13, .37, .71):
                guard()
                efold = float(grid[index] + fraction * (grid[index + 1] - grid[index]))
                matrix = np.zeros((size, size))
                matrix[saved["rows"], saved["columns"]] = core_curve(efold)
                energy.blocks(efold)
                actual = energy.comparison(matrix)
                excess = float(np.max(actual - saved["comparison"][index]))
                maximum_excess = max(maximum_excess, excess)
                tolerance = ALGEBRA * max(sup(saved["comparison"][index]), 1.)
                check(model + ":matrix-envelope:" + str(index) + ":" + str(fraction), excess <= tolerance, excess)
                source = source_curve(efold)
                norms = np.array([np.linalg.norm(source[energy.heavy]) if len(energy.heavy) else 0., np.linalg.norm(source[energy.rest])])
                check(model + ":force-envelope:" + str(index) + ":" + str(fraction),
                      np.all(norms <= saved["forcing"][index] + ALGEBRA * max(sup(saved["forcing"][index]), 1e-80)))
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        with np.load(reference_path) as archive:
            reference = {name: archive[name].copy() for name in ("efold", "diagnostics", "values", "value_names")}
        physical = load(ADJOINT / "response-v2/adjoints" / (model + "-physical-sources.npz"))
        primitive = MetricPrimitive(system, reference)
        initial_direction = primitive.vector(float(grid[0]), 1.)[0]
        transform, _, _, _ = energy.blocks(float(grid[0]))
        initial_vector = transform @ initial_direction * physical["momentum"][0]
        expected_initial = np.array([np.linalg.norm(initial_vector[energy.heavy]) if len(energy.heavy) else 0., np.linalg.norm(initial_vector[energy.rest])])
        check(model + ":nonzero-initial-primitive", relative(expected_initial - saved["initial"], expected_initial) < ALGEBRA)
        final_direction = primitive.vector(float(grid[-1]), 1.)[0]
        _, inverse, _, _ = energy.blocks(float(grid[-1]))
        dual = saved["readout"] @ inverse
        expected_norm = np.stack([np.linalg.norm(dual[:, energy.heavy], axis=1) if len(energy.heavy) else np.zeros(2),
                                  np.linalg.norm(dual[:, energy.rest], axis=1)], axis=1)
        check(model + ":physical-terminal-readout", relative(expected_norm - saved["readout_norm"], expected_norm) < ALGEBRA)
        expected_boundary = abs(saved["readout"] @ final_direction * physical["momentum"][-1])
        check(model + ":terminal-primitive", relative(expected_boundary - saved["terminal_boundary"], expected_boundary) < ALGEBRA)
        reconstructed, transition = propagate(grid, saved["comparison"], saved["forcing"], saved["initial"])
        check(model + ":comparison-replay", relative(reconstructed - saved["final"], saved["final"]) < ALGEBRA)
        check(model + ":transition-replay", relative(transition - saved["transition"], saved["transition"]) < ALGEBRA)
        bound = saved["readout_norm"] @ reconstructed + expected_boundary
        check(model + ":bound-replay", relative(bound - report["prediction"]["bound"], bound) < ALGEBRA)
        with np.load(POISSON / "evolution" / (model + "-poisson-spatial.npz")) as archive:
            target = archive["values"][-1]
        names = reference["value_names"].tolist()
        selected = [names.index("D"), names.index("delta_c")]
        scales = np.max(abs(reference["values"][:, selected]), axis=0)
        measured = (target[selected] - reference["values"][-1, selected]) / scales
        check(model + ":forward-readback", np.array_equal(measured, np.asarray(report["measured"])))
        check(model + ":bound-covers", np.all(abs(measured) <= bound))
        for name, value in report["errors"].items():
            check(model + ":qualification:" + name, value < (ALGEBRA if name == "bernstein_reconstruction" else GATE), value)
        check(model + ":exponential-substep", report["integration_error"] < GATE, report["integration_error"])
        del system, energy, saved, core_curve, source_curve
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "bound/validation.json", dict(passed=passed, count=len(checks), checks=checks))
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    print(LABEL, "independent validation", len(checks), "passed", passed, flush=True)
    require(passed, "preserve validation discrepancy")


if __name__ == "__main__":
    main()

