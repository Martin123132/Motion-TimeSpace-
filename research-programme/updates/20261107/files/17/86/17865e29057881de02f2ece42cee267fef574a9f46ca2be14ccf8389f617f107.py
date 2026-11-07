from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import quad
import sympy as sp


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/surface-limit'
    output.mkdir(exist_ok=False)
    substituted = sp.symbols('substituted', positive=True)
    harmonic, tension, radius, density, displacement, tide = sp.symbols('harmonic tension radius density displacement tide', positive=True)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('planar_grand_potential_factorization', substituted**4-4*substituted+3-(substituted-1)**2*(substituted**2+2*substituted+3))
    exact('fixed_volume_surface_second_variation', harmonic*(harmonic+1)/2-1-(harmonic-1)*(harmonic+2)/2)
    stiffness = tension*(harmonic-1)*(harmonic+2)
    energy = stiffness*displacement**2/2+density*tide*radius**4*displacement
    response = -density*radius**4/stiffness
    exact('liquid_surface_force_balance', sp.diff(energy, displacement).subs(displacement, response*tide))
    exact('liquid_frequency_from_kinetic_and_surface_energy', stiffness/(density*radius**3/harmonic)-harmonic*(harmonic-1)*(harmonic+2)*tension/(density*radius**3))
    sigma, quadrature_error = quad(lambda field: .5*field**(2/3)*(1-field**(2/3))*np.sqrt(field**(4/3)+2*field**(2/3)+3), 0, 1, epsabs=1e-13, epsrel=1e-13)
    static_path = ROOT/'results/static-bvp/status.json'
    mode_path = ROOT/'results/quadratic-fine/status.json'
    background_path = ROOT.parent/'self-gravity-20261003/results/fine/status.json'
    static = json.loads(static_path.read_text(encoding='utf-8'))
    modes = json.loads(mode_path.read_text(encoding='utf-8'))
    backgrounds = json.loads(background_path.read_text(encoding='utf-8'))
    rows = []
    for row in static['rows']:
        if row['cutoff_distance'] != .005:
            continue
        mode = next(value for value in modes['rows'] if value['radius'] == row['radius'])
        background = next(value for value in backgrounds['rows'] if value['radius'] == row['radius'] and value['alpha'] == 0)
        charge_radius = (3*background['charge']/(4*np.pi))**(1/3)
        susceptibility = charge_radius**8/(4*sigma)
        squared_frequency = 8*sigma/charge_radius**3
        rows.append({'support_radius': row['radius'], 'charge_volume_radius': charge_radius,
                     'liquid_susceptibility': susceptibility, 'field_susceptibility': row['susceptibility'],
                     'field_over_liquid_susceptibility': row['susceptibility']/susceptibility,
                     'liquid_frequency': np.sqrt(squared_frequency), 'field_frequency': mode['frequencies'][0],
                     'field_over_liquid_frequency': mode['frequencies'][0]/np.sqrt(squared_frequency)})
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks,
              'exact_check_count': len(checks), 'input_hashes': {str(path): digest(path) for path in [static_path, mode_path, background_path]},
              'dimensionless_tension_from_same_potential': sigma, 'quadrature_error_estimate': quadrature_error,
              'coexistence_charge_density': 1, 'coexistence_energy_density': 1, 'coexistence_pressure': 0,
              'radius_rule': 'Charge-volume radius (3q/(4pi))^(1/3), not support radius and not fitted.',
              'scope': 'Leading incompressible large-charge approximation; comparison only, not a finite-radius identity.', 'rows': rows}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
