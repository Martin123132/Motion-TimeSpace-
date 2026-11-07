from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/tidal-mechanics'
    output.mkdir(exist_ok=False)
    quadrupole, tidal_field, response, gravity, mass, separation = sp.symbols('quadrupole tidal_field response gravity mass separation', real=True, nonzero=True)
    energy = quadrupole**2/(4*response)+quadrupole*tidal_field/2
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('stationary_quadrupole_matches_computed_linear_response', sp.diff(energy, quadrupole).subs(quadrupole, -response*tidal_field))
    exact('eliminated_conservative_tidal_energy', energy.subs(quadrupole, -response*tidal_field)+response*tidal_field**2/4)
    point_tide = gravity*mass/separation**3*sp.diag(1, 1, -2)
    exact('point_companion_tidal_tensor_norm', sp.trace(point_tide*point_tide)-6*(gravity*mass/separation**3)**2)
    pair_energy = -3*gravity*response*mass**2/separation**6
    newton = -gravity*mass**2/separation
    exact('identical_pair_static_tidal_energy_ratio', pair_energy/newton-3*response/separation**5)
    exact('identical_pair_static_tidal_force_ratio', sp.diff(pair_energy, separation)/sp.diff(newton, separation)-18*response/separation**5)
    tidal_path = ROOT/'results/refined/status.json'
    binary_path = ROOT.parent/'collective-motion-20261004/results/binary-scales/status.json'
    tide = json.loads(tidal_path.read_text(encoding='utf-8'))
    binary = json.loads(binary_path.read_text(encoding='utf-8'))
    row = next(entry for entry in tide['rows'] if entry['nominal_flat_compactness'] == .03)
    assert row['alpha'] == binary['fixed_alpha'] and row['radius'] == binary['body_radius']
    assert abs(row['geometric_mass']/(row['alpha']*binary['body_adm_energy']/(4*np.pi))-1) < 1e-14
    rows = []
    for configuration in binary['rows']:
        distance = configuration['separation']
        ratio = 3*row['geometric_tidal_lambda']/distance**5
        epsilon = -row['geometric_mass']/distance**3*np.sqrt(4*np.pi/5)
        displacement = abs(epsilon*row['surface_displacement_per_unit_tide'])*np.sqrt(5/(4*np.pi))
        rows.append({'separation_over_radius': configuration['separation_over_radius'],
                     'static_tidal_energy_over_newtonian_magnitude': ratio,
                     'static_tidal_force_over_newtonian_magnitude': 6*ratio,
                     'static_pair_tidal_energy': ratio*configuration['interaction_energy'],
                     'maximum_surface_displacement_over_radius': displacement/row['radius'],
                     'binary_time_dependence_or_resonance_tested': False})
    result = {'state': 'complete', 'script_sha256': digest(__file__),
              'input_hashes': {str(path): digest(path) for path in [tidal_path, binary_path]},
              'checks': checks, 'exact_check_count': len(checks), 'rows': rows,
              'geometric_tidal_lambda': row['geometric_tidal_lambda'],
              'physical_operator': 'S_tide=(lambda_geom_physical/(4*G_R))*integral E_munu E^munu d_tau',
              'scope': 'Zero-frequency conservative response matching; applying instantaneous values to an orbit additionally requires its frequency well below the coupled gravitational quadrupole modes.',
              'gravitating_quadrupole_gap_calculated': False, 'physical_scale_fitted': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
