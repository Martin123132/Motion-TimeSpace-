from common import ROOT, CLOSURE, modest, require, read, write, digest
import sympy as sy


def main():
    modest()
    owner = read(ROOT / "balance-corrected/balance-result.json")
    require(owner["numerical_passed"], "validated diagnostic required")
    hubble_old, hubble_new, scale = sy.symbols("H0 H1 a", positive=True)
    identities, changes, true_density, true_pressure, density_rates = {}, [], [], [], []
    for label in ("slow", "heavy"):
        field, velocity, correction, velocity_correction, field_n, velocity_n, mass = sy.symbols(label + "_phi " + label + "_v " + label + "_u " + label + "_w " + label + "_phiN " + label + "_vN " + label + "_m", real=True)
        omega2 = (scale * mass) ** 2
        residual_field = field_n - velocity / hubble_old
        residual_velocity = velocity_n + 2 * velocity + omega2 * field / hubble_old
        correction_n = (velocity + velocity_correction) / hubble_new - velocity / hubble_old - residual_field
        velocity_correction_n = -2 * velocity_correction - omega2 * ((field + correction) / hubble_new - field / hubble_old) - residual_velocity
        repaired_field, repaired_velocity = field + correction, velocity + velocity_correction
        identities[label + "_field_kinematics"] = field_n + correction_n - repaired_velocity / hubble_new
        identities[label + "_field_dynamics"] = velocity_n + velocity_correction_n + 2 * repaired_velocity + omega2 * repaired_field / hubble_new
        rho = (velocity ** 2 + omega2 * field ** 2) / 2
        new_rho = (repaired_velocity ** 2 + omega2 * repaired_field ** 2) / 2
        new_pressure = (repaired_velocity ** 2 - omega2 * repaired_field ** 2) / 2
        change = velocity * velocity_correction + velocity_correction ** 2 / 2 + omega2 * (field * correction + correction ** 2 / 2)
        identities[label + "_exact_density_correction"] = new_rho - rho - change
        new_rho_n = repaired_velocity * (-2 * repaired_velocity - omega2 * repaired_field / hubble_new) + omega2 * repaired_field ** 2 + omega2 * repaired_field * repaired_velocity / hubble_new
        identities[label + "_background_stress_balance"] = new_rho_n + new_rho + 3 * new_pressure
        changes.append(change)
        true_density.append(new_rho)
        true_pressure.append(new_pressure)
        density_rates.append(new_rho_n)
    identities["two_field_background_balance"] = sum(density_rates) + sum(true_density) + 3 * sum(true_pressure)
    delta_h2 = sum(changes) / 3
    identities["Friedmann_difference"] = 3 * delta_h2 - sum(changes)
    results = {name: str(sy.simplify(value)) for name, value in identities.items()}
    require(all(value == "0" for value in results.values()), "exact correction identity")
    write(ROOT / "background-repair-derivation.json", dict(passed=True, identities=results, source_sha256=digest(__file__), diagnostic_sha256=digest(ROOT / "balance-corrected/balance-result.json"), previous_closeout_sha256=digest(CLOSURE / "closeout.json"), numerical_repair_executed=False, calibration_parameters_added=False, independent_variable="N=ln(a)", anchor="u=w=0 at the retained initial physical scale factor", expanding_branch="H1=sqrt(H0^2+sum(Delta R)/3)>0", clock_equation="d tau1/dN=1/H1; anchor tau1 at retained initial slice", other_background_sources="retained functions of a; their approximations remain separately audited"))
    print(dict(passed=True, exact_identities=len(results), numerical_repair_executed=False), flush=True)


if __name__ == "__main__":
    main()
