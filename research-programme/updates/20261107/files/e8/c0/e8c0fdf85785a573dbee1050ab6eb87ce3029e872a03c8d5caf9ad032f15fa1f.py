from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'eccentric-polar-source-20261005'))
from polar_source import coefficients, metric_and_boundary, quadrature_nodes, modest_process
from eccentric_source import anomaly_solution, orbit_constants, source_samples
sys.path.insert(0, str(BRANCH/'companion-source-20261004'))
from companion_system import ResponseProblem, outgoing_samples, horizon_samples, sample_vacuum, static_master_basis


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value, exclusive=False):
    with Path(path).open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)


def settings(label):
    fine = label != 'coarse'
    return {'distance': .04 if fine else .02, 'interior_tolerance': 5e-9 if fine else 2e-8,
            'exterior_tolerance': 8e-14 if fine else 3e-12,
            'far_phase': 65. if fine else 80., 'outer_order': 16 if fine else 14,
            'horizon_epsilon': 2e-6 if fine else 3e-6, 'horizon_order': 10 if fine else 8,
            'source_order': 40 if label == 'quadrature' else (32 if fine else 24),
            'source_panels_per_half': 32 if label == 'quadrature' else (24 if fine else 16),
            'orbit_tolerance': 3e-13 if fine else 3e-11}


class PolarRadiation:
    def __init__(self, chosen, eccentricity):
        self.settings = chosen
        self.body = ResponseProblem(chosen['distance'], chosen['interior_tolerance'])
        self.mass, self.radius = self.body.mass, self.body.radius
        self.eccentricity = eccentricity
        self.semilatus = 5*self.radius*(1+eccentricity)/self.mass
        self.energy, self.angular = orbit_constants(self.mass, self.semilatus, eccentricity)
        self.trajectory = anomaly_solution(self.mass, self.semilatus, eccentricity, chosen['orbit_tolerance'])
        self.period, self.phase_advance = 2*self.trajectory.sol(np.pi)[:2]
        self.omega_r = 2*np.pi/self.period
        self.omega_phi = self.phase_advance/self.period
        self.half, self.half_weights = self.source_nodes(False)
        self.full, self.full_weights = self.source_nodes(True)
        self.positions = np.unique(np.concatenate([[self.radius], self.half['radius'], self.full['radius']]))
        self.half_indices = np.searchsorted(self.positions, self.half['radius'])
        self.full_indices = np.searchsorted(self.positions, self.full['radius'])

    def source_nodes(self, full):
        chosen = self.settings
        nodes, weights = quadrature_nodes(chosen['source_order'], chosen['source_panels_per_half']*(2 if full else 1),
                                          0., 2*np.pi if full else np.pi)
        samples = source_samples(nodes, self.trajectory, self.mass, self.semilatus, self.eccentricity)
        return samples, weights*samples['time_anomaly']/self.period

    def sources(self, azimuth):
        return [coefficients(samples, self.mass, self.energy, self.angular, azimuth)
                for samples in [self.half, self.full]]

    def overlap(self, radial, frequency, sources):
        master, slope = radial[self.half_indices].T
        source = sources[0]
        terms = np.exp(1j*frequency*self.half['time'])*(source['delta']*master-source['delta_prime']*slope)
        result = 2*np.dot(self.half_weights, terms.real)
        scale = 2*np.dot(self.half_weights, np.abs(terms))
        return float(result), float(scale)

    def overlap_controls(self, radial, frequency, sources, expected):
        master, slope = radial[self.full_indices].T
        source = sources[1]
        phase = np.exp(1j*frequency*self.full['time'])
        terms = phase*(source['delta']*master-source['delta_prime']*slope)
        contraction, boundary = metric_and_boundary(self.full, source, self.mass, frequency, master, slope)
        metric_terms = -phase*source['strength']*contraction/6
        raw = np.dot(self.full_weights, terms)
        metric = np.dot(self.full_weights, metric_terms)
        scale = max(float(np.dot(self.full_weights, np.abs(terms)+np.abs(metric_terms))), 1e-300)
        return {'full_vs_half_error_over_absolute_scale': float(abs(raw-expected)/scale),
                'metric_reciprocity_error_over_absolute_scale': float(abs(raw-metric)/scale),
                'full_imaginary_error_over_absolute_scale': float(abs(raw.imag)/scale)}

    def interior(self, frequency):
        inside, solution, problem = self.body.interior(abs(frequency))
        slope = inside[1]/inside[0]
        imaginary_error = abs(slope.imag)/max(abs(slope.real), 1/self.radius)
        assert imaginary_error < 1e-12, 'Interior is not verified real/nonabsorbing.'
        report = {'body_slope': float(slope.real), 'body_slope_imaginary_error': float(imaginary_error),
                  'interior_nodes': len(solution.x), 'interior_maximum_residual': float(max(solution.rms_residuals)),
                  'interior_boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p))))}
        archive = {'spline_knots': solution.sol.x, 'spline_coefficients': solution.sol.c,
                   'parameters': solution.p, 'scales': problem.scales, 'frequency': abs(frequency)}
        return report, archive, inside

    def evaluate(self, azimuth, harmonic):
        assert azimuth in [0, 2] and (azimuth != 0 or harmonic > 0)
        frequency = azimuth*self.omega_phi+harmonic*self.omega_r
        assert frequency != 0
        positive = abs(frequency)
        chosen = self.settings
        source = self.sources(azimuth)
        outgoing, outnorm, outdiag = outgoing_samples(self.mass, positive, self.positions,
              chosen['far_phase'], chosen['outer_order'], chosen['exterior_tolerance'])
        horizon, hornorm, hord = horizon_samples(self.mass, positive, self.positions,
              chosen['horizon_epsilon'], chosen['horizon_order'], chosen['exterior_tolerance'])
        if frequency < 0:
            outnorm, hornorm = np.conj(outnorm), np.conj(hornorm)
        alpha_out = outgoing[self.radius][1].real
        alpha_horizon = horizon[self.radius][1].real
        beta_out, beta_horizon = frequency/abs(outnorm)**2, -frequency/abs(hornorm)**2
        real_outgoing = np.array([outgoing[position].real for position in self.positions])
        dirichlet = sample_vacuum(self.radius, self.positions[-1], [0., 1.], self.mass,
                                  positive, self.positions, chosen['exterior_tolerance']).real
        interior, archive, _ = self.interior(frequency)
        body_slope = interior['body_slope']
        real_source, real_scale = self.overlap(real_outgoing, frequency, source)
        dirichlet_source, dirichlet_scale = self.overlap(dirichlet, frequency, source)
        overlap_out = complex(real_source, beta_out*dirichlet_source)
        overlap_horizon = complex(real_source+(alpha_horizon-alpha_out)*dirichlet_source, beta_horizon*dirichlet_source)
        wronskian_body = complex(alpha_out-body_slope, beta_out)
        wronskian_horizon = complex(alpha_out-alpha_horizon, beta_out-beta_horizon)
        wronskian_difference = complex(alpha_horizon-body_slope, beta_horizon)
        reference_coefficient = overlap_horizon/wronskian_horizon
        delta_coefficient = -wronskian_difference*overlap_out/(wronskian_body*wronskian_horizon)
        reference_amplitude = reference_coefficient/outnorm
        delta_amplitude = delta_coefficient/outnorm
        horizon_amplitude = overlap_out/(wronskian_horizon*hornorm)
        factor = 3/(4*np.pi)*frequency**2
        reference_power, horizon_power = factor*abs(reference_amplitude)**2, factor*abs(horizon_amplitude)**2
        difference_power = factor*(2*(np.conj(reference_amplitude)*delta_amplitude).real+abs(delta_amplitude)**2)
        net_difference = difference_power-horizon_power
        retarded_action = -3/(8*np.pi)*delta_coefficient*overlap_out
        optical_scale = max(abs(difference_power)+horizon_power, 1e-300)
        direct = sample_vacuum(self.radius, self.positions[-1], [1., body_slope], self.mass,
                               positive, self.positions, chosen['exterior_tolerance']).real
        direct_source, direct_scale = self.overlap(direct, frequency, source)
        direct_amplitude = direct_source/(wronskian_body*outnorm)
        amplitude_scale = max(abs(reference_amplitude+delta_amplitude),
                 (real_scale+abs(body_slope-alpha_out)*dirichlet_scale)/abs(wronskian_body*outnorm), 1e-300)
        reconstructed_horizon = real_outgoing+(alpha_horizon-alpha_out+1j*beta_horizon)*dirichlet
        direct_horizon = np.array([horizon[position] if frequency > 0 else np.conj(horizon[position]) for position in self.positions])
        controls = [self.overlap_controls(radial, frequency, source, expected)
                    for radial, expected in [(real_outgoing, real_source), (dirichlet, dirichlet_source)]]
        wronskians = real_outgoing[:, 0]*dirichlet[:, 1]-real_outgoing[:, 1]*dirichlet[:, 0]
        row = {'eccentricity': self.eccentricity, 'azimuth': azimuth, 'harmonic': harmonic, 'reality_pair_degeneracy': 2,
               'frequency': float(frequency), 'frequency_R': float(frequency*self.radius), **interior,
               'alpha_out': float(alpha_out), 'alpha_horizon': float(alpha_horizon),
               'beta_out': float(beta_out), 'beta_horizon': float(beta_horizon),
               'body_W_magnitude': float(abs(wronskian_body)), 'BH_W_magnitude': float(abs(wronskian_horizon)),
               'source_real_basis': real_source, 'source_dirichlet_basis': dirichlet_source,
               'source_real_absolute_scale': real_scale, 'source_dirichlet_absolute_scale': dirichlet_scale,
               'BH_infinity_energy': float(reference_power), 'BH_horizon_energy': float(horizon_power),
               'body_infinity_energy': float(reference_power+difference_power),
               'difference_infinity_energy': float(difference_power), 'difference_total_energy': float(net_difference),
               'retarded_action_real': float(retarded_action.real), 'retarded_action_imag': float(retarded_action.imag),
               'optical_energy_difference': float(2*frequency*retarded_action.imag),
               'optical_angular_difference': float(2*azimuth*retarded_action.imag),
               'optical_radial_difference': float(2*harmonic*retarded_action.imag),
               'optical_error_over_component_sum': float(abs(2*frequency*retarded_action.imag-net_difference)/optical_scale),
               'direct_body_amplitude_error_over_source_scale': float(abs(direct_amplitude-reference_amplitude-delta_amplitude)/amplitude_scale),
               'Wronskian_error': float(max(abs(wronskians-1))),
               'BH_reconstruction_relative_error': float(np.max(abs(reconstructed_horizon-direct_horizon))/max(np.max(abs(direct_horizon)), 1e-300)),
               'BH_boundary_control': float(abs(-0.*overlap_out/(wronskian_horizon**2))),
               'outgoing_diagnostic': outdiag, 'horizon_diagnostic': hord}
        for prefix, amplitude in [('reference_amplitude', reference_amplitude), ('delta_amplitude', delta_amplitude),
                                  ('horizon_amplitude', horizon_amplitude), ('outgoing_norm', outnorm), ('horizon_norm', hornorm)]:
            row[prefix+'_real'], row[prefix+'_imag'] = float(amplitude.real), float(amplitude.imag)
        for key in controls[0]:
            row[key] = max(control[key] for control in controls)
        for channel in ['BH_infinity', 'BH_horizon', 'body_infinity', 'difference_infinity', 'difference_total']:
            row[channel+'_angular'] = float(azimuth*row[channel+'_energy']/frequency)
            row[channel+'_radial'] = float(harmonic*row[channel+'_energy']/frequency)
        archive.update(positions=self.positions, real_outgoing=real_outgoing, dirichlet=dirichlet, direct_body=direct,
                       half_anomaly=self.half['anomaly'], half_weights=self.half_weights)
        return row, archive

    def static(self):
        report, archive, inside = self.interior(0.)
        basis = static_master_basis(self.radius, self.mass, 1.)
        amplitudes = np.linalg.solve(basis, inside)
        response = amplitudes[1]/(3*amplitudes[0])
        assert abs(response.imag) < 1e-8
        response = float(response.real)
        decaying = np.array([static_master_basis(position, self.mass, 1.)[:, 1] for position in self.positions])
        source = self.sources(0)
        overlap, scale = self.overlap(decaying.real, 0., source)
        coefficient = 3*response*overlap/np.linalg.det(basis)
        action = -3/(16*np.pi)*coefficient*overlap
        return {'eccentricity': self.eccentricity, 'azimuth': 0, 'harmonic': 0, 'frequency': 0.,
                'reality_pair_degeneracy': 1, 'tidal_lambda': response, 'static_action_real': float(action.real),
                'static_action_imaginary_error': float(abs(action.imag)), 'energy_flux': 0., 'angular_flux': 0.,
                'source_overlap': overlap, 'source_absolute_scale': scale, **report,
                **self.overlap_controls(decaying.real, 0., source, overlap)}, archive

    def orbit_report(self):
        return {'eccentricity': self.eccentricity, 'semilatus': self.semilatus, 'mass': self.mass,
                'radius': self.radius, 'period': float(self.period), 'phase_advance': float(self.phase_advance),
                'omega_r': float(self.omega_r), 'omega_phi': float(self.omega_phi),
                'energy': float(self.energy), 'angular': float(self.angular)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--settings', choices=['coarse', 'fine', 'quadrature'], required=True)
    parser.add_argument('--plan', choices=['pilot', 'spectrum', 'extension'], required=True)
    parser.add_argument('--eccentricity', type=float, default=.3)
    parser.add_argument('--maximum', type=int, default=24)
    parser.add_argument('--minimum', type=int, default=25)
    args = parser.parse_args()
    modest_process()
    directory = ROOT/'results'/args.label
    directory.mkdir(parents=True, exist_ok=False)
    chosen = settings(args.settings)
    if args.plan == 'pilot':
        plans = [(0., [(2, 0), (0, 1), (2, 1)]), (.3, [(0, 1), (0, 2), (2, -3), (2, -2), (2, 0), (2, 1), (2, 3)])]
    elif args.plan == 'spectrum':
        plans = [(args.eccentricity, [(2, harmonic) for harmonic in range(-args.maximum, args.maximum+1)]
                                   +[(0, harmonic) for harmonic in range(1, args.maximum+1)])]
    else:
        plans = [(args.eccentricity, [(2, harmonic) for harmonic in range(-args.maximum, args.maximum+1) if abs(harmonic) >= args.minimum]
                                   +[(0, harmonic) for harmonic in range(args.minimum, args.maximum+1)])]
    start = time.perf_counter()
    inputs = {str(Path(module.__file__).resolve()): digest(Path(module.__file__)) for module in list(sys.modules.values())
              if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py' and BRANCH in Path(module.__file__).resolve().parents}
    inputs[str(BRANCH/'eccentric-polar-source-20261005/results/stage-integrity.json')] = digest(BRANCH/'eccentric-polar-source-20261005/results/stage-integrity.json')
    report = {'state': 'running', 'started_at_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'input_hashes': inputs, 'arguments': vars(args), 'settings': chosen, 'orbits': [], 'static_rows': [], 'rows': []}
    write_json(directory/'status.json', report)
    try:
        for eccentricity, modes in plans:
            engine = PolarRadiation(chosen, eccentricity)
            report['orbits'].append(engine.orbit_report())
            if args.plan != 'extension':
                row, archive = engine.static()
                report['static_rows'].append(row)
                np.savez_compressed(directory/f'static_e{eccentricity:g}.npz', **archive)
            for azimuth, harmonic in modes:
                mode_started = time.perf_counter()
                row, archive = engine.evaluate(azimuth, harmonic)
                row['elapsed_seconds'] = time.perf_counter()-mode_started
                row['archive'] = f'wave_e{eccentricity:g}_m{azimuth}_n{harmonic}.npz'
                np.savez_compressed(directory/row['archive'], **archive)
                report['rows'].append(row)
                report['elapsed_seconds'] = time.perf_counter()-start
                write_json(directory/'status.json', report)
                message = json.dumps({'completed_modes': len(report['rows']), 'e': eccentricity, 'm': azimuth, 'n': harmonic,
                                      'seconds': row['elapsed_seconds'], 'optical_error': row['optical_error_over_component_sum'],
                                      'reciprocity_error': row['metric_reciprocity_error_over_absolute_scale']})
                print(message, flush=True)
                with (directory/'log.txt').open('a', encoding='utf-8') as handle:
                    handle.write(message+'\n')
        report['state'] = 'complete'
        report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        report['elapsed_seconds'] = time.perf_counter()-start
        write_json(directory/'status.json', report)
        (directory/'COMPLETE').write_text(report['finished_at_utc']+'\n', encoding='utf-8')
    except BaseException as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        write_json(directory/'status.json', report)
        raise


if __name__ == '__main__':
    main()
