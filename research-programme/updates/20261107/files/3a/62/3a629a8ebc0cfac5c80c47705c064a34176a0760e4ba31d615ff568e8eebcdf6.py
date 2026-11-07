import sympy as sp
from step_common import *


def main():
    modest()
    folder = ROOT / 'results/derived-step'
    assert not folder.exists()
    checks = []
    frequency = sp.symbols('frequency', positive=True)
    occupation = 1 / (sp.exp(frequency) - 1)
    weight = occupation * (1 + occupation)
    potential = sp.Function('potential')(frequency)
    logarithmic = lambda value: frequency * sp.diff(value, frequency)
    spectral = weight * potential
    inherited_scalar = (logarithmic(logarithmic(spectral)) + 3 * logarithmic(spectral) + 2 * spectral
                        + frequency * (1 + 2 * occupation) * (logarithmic(spectral) + 2 * spectral)) / weight
    local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * weight
    diffusion = frequency ** 2 * sp.diff(potential, frequency, 2) + (4 * frequency - frequency ** 2 * (1 + 2 * occupation)) * sp.diff(potential, frequency)
    checks.append(dict(name='Exact weight-conjugated spectral operator',
                       passed=sp.simplify(inherited_scalar - diffusion - (2 - local) * potential) == 0))
    source = frequency ** 2 * (1 + 2 * occupation) - 4 * frequency
    checks.append(dict(name='Exact common-temperature null vector of diffusion plus plasma source',
                       passed=sp.simplify(diffusion.subs(potential, frequency).doit() + source) == 0))
    theta, wavenumber = sp.symbols('theta wavenumber', positive=True)
    principal = -1 + sp.Rational(2, 5) * theta * wavenumber ** 2
    checks.append(dict(name='High-log-frequency dipole symbol grows above the asymptotic domain',
                       passed=sp.limit(principal, wavenumber, sp.oo) == sp.oo))
    model = CollisionStep(48, 8, 4.596201578526332e-4, 5.755472902372619e-10, .001)
    symmetric = model.symmetric_photon()
    metric = model.entropy_metric
    photon_temperature = model.photon @ model.temperature_equilibrium + model.temperature_column
    checks.append(dict(name='Discrete temperature column derives from the same photon operator',
                       passed=bool(np.max(abs(photon_temperature)) < 1e-10), value=float(np.max(abs(photon_temperature)))))
    rng = np.random.default_rng(7207)
    for index in range(5):
        potential_array = rng.normal(size=model.size) + 1j * rng.normal(size=model.size)
        temperature = rng.normal() + 1j * rng.normal()
        velocity = rng.normal() + 1j * rng.normal()
        collision = model.source(potential_array, temperature, velocity)
        matter_temperature = -(model.energy @ collision) / model.heat_capacity
        matter_velocity = -(model.flux @ collision) / model.inertia
        actual = (np.vdot(potential_array, metric * collision)
                  + model.heat_capacity * temperature.conjugate() * matter_temperature
                  + model.inertia * velocity.conjugate() * matter_velocity).real
        relative = potential_array - model.temperature_equilibrium * temperature - model.velocity_equilibrium * velocity
        expected = np.vdot(relative, metric * (model.photon @ relative)).real
        error = float(abs(actual - expected) / max(abs(expected), 1e-100))
        checks.append(dict(name='Coupled photon/plasma entropy identity ' + str(index),
                           passed=bool(error < 1e-10 and expected <= 0), value=error, entropy_derivative=float(expected)))
        invariants = model.invariants(collision, matter_temperature, matter_velocity)
        invariant_error = float(np.max(abs(invariants)))
        checks.append(dict(name='Independent total-species derivative conservation ' + str(index),
                           passed=invariant_error < 1e-9, value=invariant_error))
    potential_array = .1 * rng.normal(size=model.size).astype(complex)
    temperature, velocity = .2 + 0j, .03 + 0j
    source_value = model.source(potential_array, temperature, velocity)
    step = .01
    updated = model.solve(2 / step, 2 * potential_array / step + source_value,
                          2 * temperature / step - (model.energy @ source_value) / model.heat_capacity,
                          2 * velocity / step - (model.flux @ source_value) / model.inertia)
    average = [(left + right) / 2 for left, right in zip([potential_array, temperature, velocity], updated)]
    average_collision = model.source(*average)
    production = (np.vdot(average[0], metric * average_collision)
                  - average[1].conjugate() * (model.energy @ average_collision)
                  - average[2].conjugate() * (model.flux @ average_collision)).real
    entropy_change = model.entropy(*updated) - model.entropy(potential_array, temperature, velocity)
    error = float(abs(entropy_change - step * production) / max(abs(entropy_change), 1e-100))
    checks.append(dict(name='Midpoint discrete entropy change equals derived dissipation',
                       passed=bool(error < 1e-9 and entropy_change <= 0), value=error))
    checks.append(dict(name='Weighted spectral matrix symmetry',
                       passed=float(np.max(abs((symmetric - symmetric.T).data))) < 1e-10))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        analytic_schur_elimination_not_algebraic_temperature_closure=True,
                        equilibrium_subtraction_is_exact_linear_change_of_variables=True,
                        entropy_theorem_requires_nonpositive_resolved_operator=True,
                        truncated_anisotropic_FP_not_uniformly_well_posed_for_arbitrarily_fine_spectra=True,
                        coarse_resolved_control_does_not_prove_full_transfer_accuracy=True), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
