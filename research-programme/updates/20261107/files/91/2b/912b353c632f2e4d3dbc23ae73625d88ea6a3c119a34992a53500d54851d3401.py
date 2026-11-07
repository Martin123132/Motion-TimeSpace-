from common import *
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from primitive_math import MetricPrimitive
from forcing_math import explicit, symbolic
import numpy as np


def main():
    modest()
    check_parent()
    (ROOT / "qualification-contexts").mkdir(exist_ok=False)
    write(ROOT / "qualification-inputs.json", dict(sources=frozen_sources(), parent_seal=PARENT_SEAL,
                                                 numerical=GATE, algebra=ALGEBRA))
    write(ROOT / "symbolic.json", symbolic())
    reports = []
    for model in ("heavy", "cold"):
        record = read(LATEST / LABEL / (model + "-channels.json"))["coefficient_input"]
        require(digest(record["path"]) == record["sha256"], "saved coefficients")
        packet = load(record["path"])
        operator = CompactAdjoint(packet)
        system = open_owned(model, "qualification-contexts")
        energy = PhysicalEnergyMap(system)
        reference = load(POISSON / "evolution" / (model + "-gr.npz"))
        primitive = MetricPrimitive(system, reference)
        errors, algebra, rows = {}, {}, []
        def check(name, value, exact=False):
            target = algebra if exact else errors
            target[name] = max(target.get(name, 0.), float(value))
        grid = packet["efold"]
        for index in np.unique(np.linspace(3, len(grid) - 5, 97, dtype=int)):
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            calculated = explicit(system, energy, efold)
            derived = calculated["derived"]
            transform = derived["transform"]
            core, _, _, _, injection, _ = operator.blocks(efold, 0)
            matrix = transform @ core @ derived["inverse"] + derived["derivative"]
            free = matrix - np.outer(derived["psi_injection"], derived["psi"]) - np.outer(derived["phi_injection"], derived["phi_rate"])
            expected_commutator = free @ derived["phi_injection"] - calculated["phi_rate"]
            check("free_commutator", relative(calculated["commutator"] - expected_commutator, expected_commutator))
            product_scale = max(np.linalg.norm(derived["density"]) * np.linalg.norm(calculated["commutator"]), 1e-80)
            check("density_contraction", abs(derived["density"] @ calculated["commutator"] - calculated["contraction"]) / product_scale, True)
            check("phase_free_contraction_bound", max(0., abs(calculated["contraction"]) - calculated["contraction_upper"]) / max(calculated["contraction_upper"], 1e-80), True)
            direction, rate, denominator = primitive.vector(efold, 1.)
            hubble = derived["hubble"]
            point = system.context["point"](efold)
            observed = system.context["observe"](point[11], system.zero_native)
            enthalpy = observed[0] + observed[1]
            mixing = -3 * (hubble + 3 * hubble * enthalpy / (2 * system.wave**2)) / (system.wave * denominator)
            original_shear = injection[:, 0] + mixing * injection[:, 1]
            original_current = original_shear + rate - core @ direction
            actual_current = transform @ original_current
            actual_shear = transform @ original_shear
            check("original_current_drive", relative(calculated["current"] - actual_current, actual_current))
            check("original_shear_drive", relative(calculated["shear"] - actual_shear, actual_shear))
            product_rule = calculated["shear"] + matrix @ calculated["primitive"] - calculated["primitive_rate"]
            check("product_rule_current", relative(calculated["current"] - product_rule, product_rule))
            step = .08 * min(grid[index] - grid[index - 1], grid[index + 1] - grid[index])
            def difference(width):
                values = [explicit(system, energy, efold + multiplier * width)["primitive"] for multiplier in (-2, -1, 1, 2)]
                return (values[0] - 8 * values[1] + 8 * values[2] - values[3]) / (12 * width)
            numerical = difference(step)
            half_step = difference(step / 2)
            check("primitive_derivative", relative(numerical - calculated["primitive_rate"], calculated["primitive_rate"]))
            check("primitive_derivative_step", relative(numerical - half_step, calculated["primitive_rate"]))
            rows.append(dict(efold=efold, contraction=calculated["contraction"],
                             contraction_upper=calculated["contraction_upper"],
                             current_norm=float(np.linalg.norm(calculated["current"])),
                             shear_norm=float(np.linalg.norm(calculated["shear"]))))
        passed = max(errors.values()) < GATE and max(algebra.values()) < ALGEBRA
        report = dict(model=model, passed=passed, errors=errors, algebra=algebra, rows=rows,
                      coefficient_input=record, new_physical_ode_solves=0)
        write(ROOT / (model + "-qualified.json"), report)
        print(LABEL, model, "forcing identities", passed, errors, algebra, flush=True)
        require(passed, "preserve forcing derivation discrepancy")
        reports.append(report)
        del system, operator, energy, reference, packet
    for path, expected in read(ROOT / "qualification-inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen qualification source")
    check_parent()
    write(ROOT / "qualification.json", dict(passed=True, reports=reports))


if __name__ == "__main__":
    main()
