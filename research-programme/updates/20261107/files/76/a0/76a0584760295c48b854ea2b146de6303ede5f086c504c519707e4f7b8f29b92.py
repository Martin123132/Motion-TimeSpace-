from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from time import perf_counter
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-radial-time-forcing-derivation-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.own(evidence.root / 'DERIVATION-20260928-exact-background-radial-time-forcing.md')
        radius, lapse, metric, coupling, source_mass, density, velocity = sp.symbols('R N F kappa ms rho V', positive=True)
        kinetic, gradient, gram = sp.symbols('T2 G2 H')
        rates = sp.symbols('T2dot G2dot Hdot rhodot Vdot')
        clock = sp.sqrt(lapse**2 - velocity**2 / metric)
        energy = kinetic / (2 * lapse**2 * metric) + gradient / 2 + gram
        mass_rhs = coupling * radius**2 * metric * energy + coupling * source_mass * density * sp.sqrt(metric) * lapse / clock
        lapse_rhs = coupling * radius * energy + coupling * source_mass * density * velocity**2 / (radius * lapse * metric**sp.Rational(3, 2) * clock)
        derivative_density = rates[0] / (2 * lapse**2 * metric) + rates[1] / 2 + rates[2]
        derived_mass = coupling * radius**2 * metric * derivative_density
        derived_mass += coupling * source_mass * sp.sqrt(metric) * lapse / clock * rates[3]
        derived_mass += coupling * source_mass * density * lapse * velocity / (sp.sqrt(metric) * clock**3) * rates[4]
        derived_lapse = coupling * radius * derivative_density
        derived_lapse += coupling * source_mass * velocity**2 / (radius * lapse * metric**sp.Rational(3, 2) * clock) * rates[3]
        derived_lapse += coupling * source_mass * density / (radius * lapse * metric**sp.Rational(3, 2)) * (2 * velocity / clock + velocity**3 / (metric * clock**3)) * rates[4]
        for name, original, derived in [('mass', mass_rhs, derived_mass), ('log_lapse', lapse_rhs, derived_lapse)]:
            exact = sum(sp.diff(original, value) * rate for value, rate in zip([kinetic, gradient, gram, density, velocity], rates))
            evidence.check(name + ':symbolic_all_input_columns', sp.simplify(exact - derived) == 0)
        count = 73
        radius_values = np.linspace(5.19, 6.81, count)
        mass_values = .7 + .002 * np.linspace(0, 1, count)
        lapse_values = -.13 + .002 * np.sin(radius_values)
        fields = [1e-5 * (1 + np.sin(radius_values)**2), 1e-4 * (1 + np.cos(radius_values)**2),
            1e-7 * np.ones(count), np.linspace(0, 2, count), np.linspace(-.03, .03, count)]
        changes = [np.cos((index + 1) * radius_values) * 1e-4 for index in range(5)]
        geometric = np.stack([np.sin(radius_values) * 1e-4, np.cos(radius_values) * 1e-4])
        step = 1e-24
        forcing = explicit_time_forcing(radius_values, mass_values, lapse_values, fields[3], fields[4], *changes, .1, .003)
        original, jacobian = radial_rhs(radius_values, mass_values, lapse_values, *fields, .1, .003, True)
        total = forcing + np.einsum('abn,bn->an', jacobian, geometric)
        full_complex = radial_rhs(radius_values, mass_values + 1j * step * geometric[0],
            lapse_values + 1j * step * geometric[1], *[value + 1j * step * change for value, change in zip(fields, changes)], .1, .003).imag / step
        error = float(np.max(abs(total - full_complex)))
        evidence.check('full_complex_time_derivative', error <= 5e-14 * np.max(abs(total)) + 1e-25, error)
        for index in range(5):
            direction = [np.zeros(count) for unused in range(5)]
            direction[index] = changes[index]
            column = explicit_time_forcing(radius_values, mass_values, lapse_values, fields[3], fields[4], *direction, .1, .003)
            checked = radial_rhs(radius_values, mass_values, lapse_values,
                *[value + 1j * step * change for value, change in zip(fields, direction)], .1, .003).imag / step
            discrepancy = float(np.max(abs(column - checked)))
            evidence.check('complex_input_column:' + str(index), discrepancy <= 5e-14 * np.max(abs(column)) + 1e-25, discrepancy)
        evidence.check('zero_source_density_and_zero_velocity_finite', np.isfinite(forcing).all() and fields[3][0] == 0 and fields[4][count // 2] == 0)
        output = evidence.output / 'local-forcing-verification.npz'
        np.savez_compressed(output, radius=radius_values, forcing=forcing, total=total, independently_differentiated=full_complex)
        evidence.own(output, 'outputs')
        evidence.report.update(seconds=perf_counter() - started,
            result='Exact local radial source-forcing derivative derived and implemented',
            moving_interface_density_projection_implemented=False,
            complete_background_metric_time_tangent_computed=False,
            maximum_complex_difference=error)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
