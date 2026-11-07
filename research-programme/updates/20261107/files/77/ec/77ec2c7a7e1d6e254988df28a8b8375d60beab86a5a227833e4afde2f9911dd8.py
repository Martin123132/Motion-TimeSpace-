from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import psutil


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-gravity-stability-20261003'))
from test_radial_energy import Profile, Quadrature


def digest(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/flat-motion'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'script_sha256': digest(__file__), 'source_seal_sha256': digest(BRANCH/'self-gravity-20261003/results/stage-integrity.json'),
              'rows': [], 'sources': []}
    try:
        for radius in [8., 20., 80.]:
            profile = Profile(radius, 0.)
            report['sources'].append({'path': str(profile.path), 'sha256': digest(profile.path)})
            for cells, order in [(256, 24), (512, 48)]:
                quadrature = Quadrature(profile.radius, cells, 8)
                positions, radial_weights = quadrature.position, quadrature.weights
                amplitude, gradient, mass, metric, xi, rotation = profile.values(positions)
                assert np.allclose(metric, 1.) and np.allclose(xi, 1.)
                potential = .375*amplitude**(4/3)+.125*amplitude**4
                frequency = profile.frequency
                density = .5*gradient**2+.5*frequency**2*amplitude**2+potential
                radial_pressure = .5*gradient**2+.5*frequency**2*amplitude**2-potential
                tangential_pressure = -.5*gradient**2+.5*frequency**2*amplitude**2-potential
                radial_measure = 4*np.pi*radial_weights*positions**2
                energy = float(radial_measure@density)
                charge = float(radial_measure@(frequency*amplitude**2))
                pressure_trace = float(radial_measure@(radial_pressure+2*tangential_pressure))
                cosine, angular_weights = np.polynomial.legendre.leggauss(order)
                measure = radial_measure[:, None]*angular_weights[None, :]/2
                field = amplitude[:, None]
                parallel = gradient[:, None]*cosine[None, :]
                transverse_squared = gradient[:, None]**2*(1-cosine[None, :]**2)
                boosts = []
                for speed in [0., .1, .3, .6, .8]:
                    gamma = 1/np.sqrt(1-speed**2)
                    field_time, field_axial = -gamma*speed*parallel, gamma*parallel
                    phase_time, phase_axial = gamma*frequency, -gamma*speed*frequency
                    lab_energy = .5*(field_time**2+field_axial**2+transverse_squared+field**2*(phase_time**2+phase_axial**2))+potential[:, None]
                    lab_momentum = -field_time*field_axial-field**2*phase_time*phase_axial
                    lab_lagrangian = .5*(field_time**2-field_axial**2-transverse_squared+field**2*(phase_time**2-phase_axial**2))-potential[:, None]
                    lab_charge = field**2*phase_time
                    integrated_energy = float(np.sum(measure*lab_energy)/gamma)
                    integrated_momentum = float(np.sum(measure*lab_momentum)/gamma)
                    integrated_charge = float(np.sum(measure*lab_charge)/gamma)
                    integrated_lagrangian = float(np.sum(measure*lab_lagrangian)/gamma)
                    routhian = integrated_lagrangian-charge*frequency/gamma
                    boosts.append({'speed': speed, 'energy': integrated_energy, 'momentum': integrated_momentum,
                                   'relative_energy_lorentz_error': abs(integrated_energy/(gamma*energy)-1),
                                   'momentum_error_over_gamma_energy': abs(integrated_momentum-gamma*speed*energy)/(gamma*energy),
                                   'relative_charge_error': abs(integrated_charge/charge-1),
                                   'relative_fixed_charge_routhian_error': abs(routhian/(-energy/gamma)-1),
                                   'relative_mass_shell_error': abs((integrated_energy**2-integrated_momentum**2)/energy**2-1)})
                exchange = []
                for separation_factor in [1.05, 1.25, 2., 5., 10.]:
                    separation = separation_factor*(20.+radius)
                    separation_squared = separation**2+positions[:, None]**2+2*separation*positions[:, None]*cosine[None, :]
                    inverse_distance = separation_squared**(-.5)
                    force_kernel = (separation+positions[:, None]*cosine[None, :])*separation_squared**(-1.5)
                    source = density+radial_pressure+2*tangential_pressure
                    scalar_energy_kernel = float(np.sum(measure*source[:, None]*inverse_distance))
                    force_integral = float(np.sum(measure*source[:, None]*force_kernel))
                    exchange.append({'separation': separation, 'surface_gap': separation-20.-radius,
                                     'interaction_energy_over_minus_G_source_mass': scalar_energy_kernel,
                                     'force_magnitude_over_G_source_mass': force_integral,
                                     'relative_energy_monopole_error': abs(scalar_energy_kernel/(energy/separation)-1),
                                     'relative_force_monopole_error': abs(force_integral/(energy/separation**2)-1)})
                row = {'flat_radius': radius, 'radial_cells': cells, 'angular_order': order,
                       'rest_energy': energy, 'charge': charge, 'integrated_pressure_trace': pressure_trace,
                       'relative_laue_residual': abs(pressure_trace)/energy,
                       'relative_rest_energy_source_difference': abs(energy/profile.row['adm_energy']-1),
                       'naive_unreduced_action_mass_fraction': (energy-frequency*charge)/energy,
                       'boosts': boosts, 'extended_source_exchange': exchange}
                report['rows'].append(row)
                print(json.dumps({'radius': radius, 'cells': cells, 'laue': row['relative_laue_residual'],
                                  'max_boost_error': max(item['relative_energy_lorentz_error'] for item in boosts),
                                  'max_force_error': max(item['relative_force_monopole_error'] for item in exchange)}), flush=True)
                (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        assert all(row['relative_laue_residual'] < 1e-7 for row in report['rows'])
        assert all(item['relative_force_monopole_error'] < 1e-7 for row in report['rows'] for item in row['extended_source_exchange'])
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
