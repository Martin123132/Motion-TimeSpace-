from __future__ import annotations

import mpmath as mp

from analyze_actions import mp_action, mp_constants
from secular import ROOT, digest, modest_process, read_json, save_report


def main():
    modest_process()
    mp.mp.dps = 60
    analysis_path = ROOT/'results/analysis/status.json'
    analysis = read_json(analysis_path)
    checks, step_tests, newtonian_tests = [], [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'value': float(error), 'tolerance': tolerance,
                       'passed': bool(abs(error) < tolerance)})

    for geometry in analysis['geometry_tests'][:3]:
        rows = analysis['main_rates']+analysis['small_rates']
        chosen = next(row for row in rows if row['eccentricity'] == geometry['eccentricity']
                      and row['semilatus'] == geometry['semilatus'] and row['channel'] == 'BH')
        for key in ['Omega_r', 'Omega_phi']:
            target = mp.mpf(geometry[key])
            check(f'independent period {geometry["eccentricity"]}:{key}',
                  (mp.mpf(chosen[key])-target)/target, 2e-12)
        target = mp.mpf(geometry['action'])
        check(f'independent action {geometry["eccentricity"]}',
              (mp.mpf(chosen['specific_radial_action'])-target)/target, 2e-12)
    for row in analysis['main_rates']:
        mass, semilatus, squared = map(mp.mpf, map(str, [row['mass'], row['semilatus'], row['eccentricity']**2]))
        pdot, zdot = map(mp.mpf, map(str, [row['semilatus_rate_per_mu'], row['squared_eccentricity_rate_per_mu']]))
        Edot, hdot = map(mp.mpf, map(str, [row['energy_rate_per_mu'], row['angular_rate_per_mu']]))
        step = mp.mpf('1e-4')*semilatus/abs(pdot)
        if squared:
            step = min(step, mp.mpf('1e-4')*squared/abs(zdot))
        energy, angular = mp_constants(mass, semilatus, squared)
        errors = []
        for chosen_step in [step, step/2]:
            new_energy, new_angular = mp_constants(mass, semilatus+chosen_step*pdot, squared+chosen_step*zdot)
            errors.append([float(abs(new_energy-energy-chosen_step*Edot)/abs(chosen_step*Edot)),
                           float(abs(new_angular-angular-chosen_step*hdot)/abs(chosen_step*hdot))])
        for index, label in enumerate(['energy', 'angular']):
            ratio = errors[1][index]/errors[0][index]
            check(f'finite step second-order remainder {row["eccentricity"]}:{row["channel"]}:{label}',
                  ratio-.5, .01)
        step_tests.append({'eccentricity': row['eccentricity'], 'channel': row['channel'],
                           'scaled_step': str(step), 'relative_errors': errors,
                           'interpretation': 'Single frozen-rate Euler step in tau=mu*t, not an integrated inspiral'})
    for eccentricity in ['0.01', '0.3', '0.6']:
        squared = mp.mpf(eccentricity)**2
        deviations = []
        for semilatus in [mp.mpf('10000'), mp.mpf('1000000')]:
            exact_action = mp_action(mp.mpf(1), semilatus, squared)
            kepler_action = mp.sqrt(semilatus)*(1/mp.sqrt(1-squared)-1)
            deviations.append(float(abs(exact_action/kepler_action-1)))
        check(f'Newtonian action large radius {eccentricity}', deviations[1], 2e-6)
        check(f'Newtonian action first inverse-p correction {eccentricity}', deviations[1]/deviations[0]-.01, .001)
        newtonian_tests.append({'eccentricity': eccentricity, 'semilatus_values': [10000, 1000000],
                                'relative_deviations': deviations})
    for row in analysis['circular_limits']:
        check(f'limit damping sign {row["channel"]}', 0 if row['small_pair_damping_limit'] < 0 else 1, .5)
    inputs = [analysis_path, ROOT/'analyze_actions.py', ROOT/'secular.py']
    save_report(ROOT/'results/physical-limits', __file__, {'checks': checks, 'step_tests': step_tests,
                'newtonian_tests': newtonian_tests, 'input_hashes': {str(path): digest(path) for path in inputs}})
    failed = [row for row in checks if not row['passed']]
    print({'checks': len(checks), 'failed': failed, 'newtonian_tests': newtonian_tests})
    assert not failed


if __name__ == '__main__':
    main()
