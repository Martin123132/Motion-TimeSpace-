from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import mpmath as mp
import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/charge-coexistence"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    checks = []

    def check(name, expression):
        assert sym.factor(expression) == 0, (name, expression)
        checks.append({"name": name, "passed": True})

    coordinate = sym.symbols("coordinate", nonnegative=True)
    amplitude, chemical, charge_density, potential = sym.symbols("amplitude chemical charge_density potential", positive=True)
    velocity = sym.symbols("velocity", real=True)
    barrier = (3 * coordinate**2 + coordinate**6 - 4 * coordinate**3) / 4
    factorized = coordinate**2 * (coordinate - 1)**2 * (coordinate**2 + 2 * coordinate + 3) / 4
    check("global_nonnegative_effective_potential", barrier - factorized)
    check("energy_charge_square_completion",
          amplitude**2 * velocity**2 / 2 + potential - chemical * amplitude**2 * velocity
          - (amplitude**2 * (velocity - chemical)**2 / 2 + potential - chemical**2 * amplitude**2 / 2))
    check("fixed_local_charge_lower_bound", charge_density**2 / (2 * amplitude**2) + potential - chemical * charge_density
          - ((charge_density - chemical * amplitude**2)**2 / (2 * amplitude**2) + potential - chemical**2 * amplitude**2 / 2))
    mean_charge, fraction, critical_charge = sym.symbols("mean_charge fraction critical_charge", positive=True)
    mixture_energy = fraction * chemical * critical_charge
    check("mixture_saturates_bulk_energy_bound", mixture_energy.subs(fraction, mean_charge / critical_charge) - chemical * mean_charge)
    check("bulk_coexistence_pressure", mean_charge * sym.diff(chemical * mean_charge, mean_charge) - chemical * mean_charge)
    check("degenerate_endpoint_zero", barrier.subs(coordinate, 1))
    check("degenerate_endpoint_stationary", sym.diff(barrier, coordinate).subs(coordinate, 1))

    estimates = []
    for digits in [50, 80]:
        mp.mp.dps = digits
        initial_amplitude = mp.mpf(10)
        initial_ratio = mp.mpf(2)
        coupling = initial_amplitude**(mp.mpf(2) / 3) / 3
        quartic = mp.mpf(1) / 150
        critical_amplitude = (coupling / quartic)**(mp.mpf(3) / 8)
        critical_chemical = mp.sqrt(2 * coupling * critical_amplitude**(-mp.mpf(2) / 3))
        critical_charge_value = critical_chemical * critical_amplitude**2
        integral_z = mp.quad(lambda value: value**mp.mpf("1.5") * (1 - value) * mp.sqrt(value**2 + 2 * value + 3), [0, mp.mpf(".5"), 1])
        tension = mp.mpf("1.5") * mp.sqrt(coupling / 2) * critical_amplitude**(mp.mpf(5) / 3) * integral_z
        def alternate_integrand(value):
            mapped = value**(mp.mpf(2) / 3)
            return mp.sqrt(coupling / 2) * critical_amplitude**(mp.mpf(5) / 3) * mapped * (1 - mapped) * mp.sqrt(mapped**2 + 2 * mapped + 3)
        alternate = mp.quad(alternate_integrand, [0, mp.mpf(".5"), 1])
        relative = abs(tension - alternate) / tension
        assert relative < mp.mpf("1e-40")
        estimates.append({"digits": digits, "critical_amplitude": str(critical_amplitude),
                          "critical_chemical_potential": str(critical_chemical),
                          "critical_charge_density": str(critical_charge_value),
                          "critical_bulk_energy_density": str(critical_chemical * critical_charge_value),
                          "scale_factor_at_coexistence": str((100 / critical_charge_value)**(mp.mpf(1) / 3)),
                          "planar_grand_potential_surface_tension": str(tension),
                          "independent_variable_quadrature_relative_error": str(relative)})
    assert abs(mp.mpf(estimates[0]["planar_grand_potential_surface_tension"]) / mp.mpf(estimates[1]["planar_grand_potential_surface_tension"]) - 1) < mp.mpf("1e-45")
    prior = json.loads((ROOT / "results/derivation/status.json").read_text(encoding="utf-8"))
    assert abs(float(estimates[-1]["scale_factor_at_coexistence"]) - prior["homogeneous_example"]["a_at_y1_from_y2_a1"]) < 1e-14
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks, "exact_check_count": len(checks), "quadrature_estimates": estimates,
        "bulk_theorem": "E >= mu_star |Q|; vacuum/critical-phase mixtures approach equality per volume in the zero-temperature nongravitating thermodynamic limit.",
        "pressureless_scope": "Equilibrated bulk mixture with negligible interface/kinetic/gravitational corrections; not a formation or cosmological-history prediction.",
        "finite_radius_droplet_solved": False, "dynamical_stability_of_droplet_proved": False,
        "derivation_sha256": hashlib.sha256((ROOT / "results/derivation/status.json").read_bytes()).hexdigest(),
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks), "critical_amplitude": float(critical_amplitude),
                      "critical_mu": float(critical_chemical), "critical_charge": float(critical_charge_value),
                      "surface_tension": float(tension)}))


if __name__ == "__main__":
    main()

