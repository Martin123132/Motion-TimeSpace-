from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent


def main():
    source = BRANCH/'self-gravity-20261003/results/fine/status.json'
    spectrum_source = BRANCH/'radial-pulsations-20261003/results/validation/status.json'
    backgrounds = json.loads(source.read_text(encoding='utf-8'))['rows']
    body = next(row for row in backgrounds if row['base_radius'] == 20 and row['nominal_flat_compactness'] == .03)
    spectra = json.loads(spectrum_source.read_text(encoding='utf-8'))['comparisons']
    spectrum = next(row for row in spectra if row['base_radius'] == 20 and row['nominal_compactness'] == .03)
    radial_frequency = spectrum['frequencies'][-1][0]
    mass, radius = body['adm_energy'], body['radius']
    coupling = body['alpha']/(4*np.pi)
    rows = []
    for separation_factor in [10., 20., 40., 80.]:
        separation = separation_factor*radius
        orbital_frequency = np.sqrt(2*coupling*mass/separation**3)
        each_speed = orbital_frequency*separation/2
        binding = -coupling*mass**2/separation
        rows.append({'separation_over_radius': separation_factor, 'separation': separation,
                     'interaction_energy': binding, 'force_magnitude': coupling*mass**2/separation**2,
                     'companion_potential_magnitude': coupling*mass/separation,
                     'circular_orbital_frequency': float(orbital_frequency), 'each_body_speed': float(each_speed),
                     'orbital_frequency_over_radial_frequency_diagnostic_only': float(orbital_frequency/radial_frequency),
                     'geometric_equal_mass_tide_scale': separation_factor**(-3),
                     'quadrupole_adiabaticity_established': False})
    output = ROOT/'results/binary-scales'
    output.mkdir(parents=True, exist_ok=False)
    result = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'source_hashes': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [source, spectrum_source]},
              'body_adm_energy': mass, 'body_charge': body['charge'], 'body_radius': radius, 'fixed_alpha': body['alpha'],
              'radial_frequency': radial_frequency, 'rows': rows,
              'scope': 'Two identical inherited R_flat20,Cnom.03 bodies, same fixed action; leading conservative matching estimates, not a simulated binary.',
              'unknown_next_response': 'Quadrupole tidal susceptibility and coupled ell=2 spectrum. A radial gap is not the gap of the tidal channel.',
              'physical_units_calibrated': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
