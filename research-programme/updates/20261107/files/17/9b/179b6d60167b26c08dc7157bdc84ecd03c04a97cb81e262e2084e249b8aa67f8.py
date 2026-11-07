from __future__ import annotations

import math

from radiation_common import *


def main():
    modest_process()
    initial = read_json(ROOT / 'results/validation/status.json')
    omega_m, _ = inherited_parameters()
    refinements = []
    for original, fraction in zip(initial['refinements'], [0., .5]):
        species = StandardSpecies(omega_m, fraction)

        def balance(efold):
            neutrino_density = math.exp(species.nu_log(efold) - 4 * efold)
            nonrel_fraction = float(species.nu_log(efold, 1))
            matter = (species.matter + fraction * omega_m) * math.exp(-3 * efold) + nonrel_fraction * neutrino_density
            radiation = species.radiation * math.exp(-4 * efold) + (1 - nonrel_fraction) * neutrino_density
            return matter - radiation

        physical_z = math.exp(-optimize.brentq(balance, -10., -6.)) - 1
        revised = {key: value for key, value in original.items() if key != 'native_zeq_is_physical_total'}
        revised.update(physical_equality_z=physical_z,
            native_zeq_includes_heavy_density=not bool(fraction),
            native_zeq_massive_neutrinos='Conventional all-relativistic equality approximation; not the pressure-resolved total.')
        refinements.append(revised)
    error = abs(refinements[0]['physical_equality_z'] / refinements[1]['physical_equality_z'] - 1)
    checks = initial['checks'] + [dict(name='same late matter and radiation budgets give same pressure-resolved equality', passed=error < 1e-12, value=error)]
    selected = {key: value for key, value in initial.items() if key not in {
        'state', 'time_utc', 'script_sha256', 'input_hashes', 'source_urls', 'camb_version',
        'checks', 'count', 'all_checks_passed', 'refinements'}}
    save('validation-final', __file__, dict(**selected, checks=checks, count=len(checks),
        all_checks_passed=all(row['passed'] for row in checks), refinements=refinements,
        supersedes='results/validation/status.json equality interpretation only',
        correction='Apply the pressure-resolved equality definition to BOTH cold and heavy branches. The native cold zeq was previously labelled exact rather than its conventional relativistic approximation. Thermal, BAO and transfer calculations are unchanged.'),
        [ROOT / 'results/validation/status.json'])
    print(dict(state='complete', checks=len(checks), equality_relative_difference=error,
        physical_equality_z=refinements[0]['physical_equality_z']), flush=True)
    assert all(row['passed'] for row in checks)


if __name__ == '__main__':
    main()

