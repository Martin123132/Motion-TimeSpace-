from __future__ import annotations

from datetime import datetime, timezone
import math
import csv

import numpy as np
from numpy.polynomial import Chebyshev
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

from common import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process, damping, imported_hashes


def projected(rows, key):
    changed = [{**row, 'BH_infinity_energy': row[key], 'BH_horizon_energy': 0.} for row in rows]
    return damping(changed, 'combined_ell2', 'BH')


def rates_at(rows):
    reference = damping(rows, 'combined_ell2', 'BH')
    outgoing = projected(rows, 'difference_infinity_energy')
    horizon = projected(rows, 'BH_horizon_energy')
    return dict(separation=rows[0]['separation_over_radius'], semilatus=rows[0]['semilatus'],
                P_BH=reference['circular_p_rate_per_mu'], G_BH=reference['Gamma_z_per_mu'],
                P_out=outgoing['circular_p_rate_per_mu'], G_out=outgoing['Gamma_z_per_mu'],
                P_H=horizon['circular_p_rate_per_mu'], G_H=horizon['Gamma_z_per_mu'])


def factors(semilatus, mass, tidal_lambda):
    shrink = -64/(5*mass**2*semilatus**3)
    damping_rate = -608/(15*mass**2*semilatus**4)
    tide, horizon = tidal_lambda/(mass*semilatus)**5, semilatus**-4
    return dict(P_BH=shrink, G_BH=damping_rate, P_out=shrink*tide,
                G_out=damping_rate*tide, P_H=shrink*horizon, G_H=damping_rate*horizon)


def kernels(values, semilatus, mass):
    shrink, gamma = values['P_BH'], values['G_BH']
    difference_shrink = values['P_out']-values['P_H']
    difference_gamma = values['G_out']-values['G_H']
    inverse_difference = -difference_shrink/(shrink*(shrink+difference_shrink))
    omega = 1/(mass*semilatus**1.5)
    return np.array([1/(mass**2*shrink), omega/(mass*shrink), gamma/shrink,
                     inverse_difference/mass**2, omega*inverse_difference/mass,
                     (difference_gamma*shrink-gamma*difference_shrink)/(shrink*(shrink+difference_shrink))])


class Curve:
    def __init__(self, nodes, mass, radius, tidal_lambda):
        self.mass, self.radius, self.tidal_lambda = mass, radius, tidal_lambda
        self.nodes = sorted(nodes, key=lambda row: row['separation'])
        coordinate = [row['separation'] for row in self.nodes]
        self.polynomials = {}
        for key in ['P_BH', 'G_BH', 'P_out', 'G_out', 'P_H', 'G_H']:
            normalized = [row[key]/factors(row['semilatus'], mass, tidal_lambda)[key] for row in self.nodes]
            self.polynomials[key] = Chebyshev.fit(coordinate, normalized, len(nodes)-1, domain=[5., 10.])

    def rates(self, separation):
        semilatus = separation*self.radius/self.mass
        normalizers = factors(semilatus, self.mass, self.tidal_lambda)
        return {key: float(polynomial(separation))*normalizers[key] for key, polynomial in self.polynomials.items()}

    def integrand(self, separation):
        semilatus = separation*self.radius/self.mass
        return kernels(self.rates(separation), semilatus, self.mass)*self.radius/self.mass

    def integral(self, separation, order=0):
        if separation == 10.:
            return np.zeros(6)
        return np.array([quad(lambda coordinate: self.integrand(coordinate)[index], 10., separation,
                              epsabs=1e-11, epsrel=2e-12, limit=100)[0] for index in range(6)])

    def export(self):
        return {key: dict(coef=value.coef.tolist(), domain=value.domain.tolist(), window=value.window.tolist())
                for key, value in self.polynomials.items()}


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    modest_process()
    inputs, reports = {}, {}

    def load(path):
        inputs[str(path)] = digest(path)
        value = read_json(path)
        assert value['state'] == 'complete', path
        return value

    for label in ['nodes-fine', 'nodes-coarse', 'gauss-fine']:
        reports[label] = load(ROOT/'results'/label/'status.json')
    tidal = load(PARENT/'results/tidal-limit/status.json')
    pole_path = BRANCH/'dynamical-tides-20261004/results/mode-edge004/status.json'
    pole = load(pole_path)
    first = reports['nodes-fine']['rows'][0]
    mass, radius = first['mass'], first['radius']
    tidal_lambda = tidal['predictions'][0]['tidal_lambda']
    eta = 1e-5
    initial_e = 1e-4
    mu = eta*mass
    nodes, curves = {}, {}
    for label, report in reports.items():
        modes = report['rows']+report['reused']
        nodes[label] = [rates_at([row for row in modes if abs(row['separation_over_radius']-separation) < 1e-10])
                        for separation in report['requested_separations']]
        if label.startswith('nodes'):
            curves[label] = Curve(nodes[label], mass, radius, tidal_lambda)
    curves['nested9-fine'] = Curve(nodes['nodes-fine'][::2], mass, radius, tidal_lambda)
    curves['nested5-fine'] = Curve(nodes['nodes-fine'][::4], mass, radius, tidal_lambda)
    final = {label: curve.integral(5.).tolist() for label, curve in curves.items()}
    weights = np.polynomial.legendre.leggauss(8)[1]
    direct_gauss = -2.5*radius/mass*sum(weight*kernels(row, row['semilatus'], mass)
                                      for weight, row in zip(weights, nodes['gauss-fine']))
    final['independent-gauss8-fine'] = direct_gauss.tolist()
    reference_curve = curves['nodes-fine']
    reference = np.array(final['nodes-fine'])
    comparisons = []
    for label, value in final.items():
        comparisons.append(dict(label=label, relative_component_errors=(abs((np.array(value)-reference)/reference)).tolist()))
    gauss_point_controls = []
    for row in nodes['gauss-fine']:
        interpolated = reference_curve.rates(row['separation'])
        gauss_point_controls.append(dict(separation=row['separation'],
              **{key: abs(interpolated[key]/row[key]-1) for key in interpolated}))

    ode = solve_ivp(lambda separation, state: reference_curve.integrand(separation)/abs(reference),
                    (10., 5.), np.zeros(6), method='DOP853', rtol=2e-12, atol=2e-13, dense_output=True)
    assert ode.success, ode.message
    ode_final = ode.y[:, -1]*abs(reference)
    trajectory = []
    for separation in np.linspace(10., 5., 41):
        value = reference_curve.integral(float(separation))
        row = dict(separation_over_radius=float(separation), semilatus=float(separation*radius/mass),
                   scaled_time_BH=float(value[0]), scaled_time_difference=float(value[3]),
                   scaled_time_body=float(value[0]+value[3]), scaled_phase_BH=float(value[1]),
                   scaled_phase_difference=float(value[4]), scaled_phase_body=float(value[1]+value[4]),
                   log_z_over_initial_BH=float(value[2]), log_z_difference=float(value[5]),
                   e_over_initial_BH=float(np.exp(value[2]/2)),
                   e_over_initial_body=float(np.exp((value[2]+value[5])/2)))
        trajectory.append(row)
    end = trajectory[-1]
    time_body = end['scaled_time_body']
    hole_same_time_radius = brentq(lambda separation: reference_curve.integral(separation)[0]-time_body,
                                  5., 10., xtol=1e-12)
    remaining = np.array([quad(lambda coordinate: reference_curve.integrand(coordinate)[index],
                              hole_same_time_radius, 5., epsabs=1e-11, epsrel=2e-12)[0]
                          for index in [0, 1]])
    equal_time_phase = end['scaled_phase_difference']+remaining[1]
    first_order_equal_time_phase = end['scaled_phase_difference']-mass/(mass*(5*radius/mass)**1.5)*end['scaled_time_difference']

    semilatus_initial, semilatus_final = 10*radius/mass, 5*radius/mass
    lambda_hat = tidal_lambda/mass**5

    def weak_primitives(semilatus):
        return np.array([-15*lambda_hat/(32*semilatus)-5*np.log(semilatus)/64,
                         -3*lambda_hat/(16*semilatus**2.5)+5/(96*semilatus**1.5),
                         -23*lambda_hat/(2*semilatus**5)+35/(24*semilatus**4)])

    weak_difference = weak_primitives(semilatus_final)-weak_primitives(semilatus_initial)
    weak_baseline = np.array([5*(semilatus_initial**4-semilatus_final**4)/256,
                             (semilatus_initial**2.5-semilatus_final**2.5)/32,
                             19/6*np.log(semilatus_final/semilatus_initial)])
    decay = -pole['sigma']['imaginary']
    pole_frequency = pole['sigma']['real']
    diagnostics = []
    modes = [(2, 0), (2, -1), (2, 1), (0, 1), (1, 0), (1, -1), (1, 1)]
    for separation in np.linspace(5., 10., 257):
        semilatus = separation*radius/mass
        values = reference_curve.rates(float(separation))
        shrink = values['P_BH']+values['P_out']-values['P_H']
        gamma = values['G_BH']+values['G_out']-values['G_H']
        p_dot, z_log_dot = mu*shrink, mu*gamma
        omega_phi = 1/(mass*semilatus**1.5)
        epicycle = np.sqrt(1-6/semilatus)
        for azimuth, harmonic in modes:
            omega = omega_phi*(azimuth+harmonic*epicycle)
            omega_prime = omega_phi*(-1.5*(azimuth+harmonic*epicycle)/semilatus+3*harmonic/(semilatus**2*epicycle))
            chirp = omega_prime*p_dot
            envelope_rate = 3*abs(p_dot)/semilatus+(abs(z_log_dot)/2 if harmonic else 0.)
            distance = abs(complex(pole_frequency-omega, -decay))
            diagnostics.append(dict(separation=float(separation), azimuth=azimuth, harmonic=harmonic,
                frequency=float(omega), frequency_rate=float(chirp),
                orbit_drift_per_radian=float(abs(p_dot)/(semilatus*omega_phi*epicycle)),
                fractional_radius_change_over_pole_memory=float(abs(p_dot)/(semilatus*decay)),
                leading_electric_envelope_memory_indicator=float(envelope_rate/decay),
                frequency_sweep_over_pole_linewidth=float(abs(chirp)/decay**2),
                detuned_first_order_pole_indicator=float(envelope_rate/distance+abs(chirp)/distance**2),
                frequency_over_known_pole=float(abs(omega)/pole_frequency)))
    indicator_keys = [key for key in diagnostics[0] if key not in ['separation', 'azimuth', 'harmonic', 'frequency', 'frequency_rate']]
    maxima = {key: max(row[key] for row in diagnostics) for key in indicator_keys}
    scale_keys = [key for key in indicator_keys if key != 'frequency_over_known_pole']
    sufficient_eta_for_indicator001 = min(eta*.01/maxima[key] for key in scale_keys)
    summary = dict(
        initial_separation_over_radius=10., final_separation_over_radius=5., mass_ratio_example=eta,
        initial_eccentricity_example=initial_e, central_mass=mass, central_radius=radius, tidal_lambda=tidal_lambda,
        scaled_time_definition='T=mu*t/M^2=eta*t/M',
        scaled_phase_definition='Phi=mu*phi/M=eta*phi; orbital phase, not doubled waveform phase',
        kernel_order=['T_BH', 'Phi_BH', 'ln(z_BH/z_initial)', 'DeltaT', 'DeltaPhi', 'Delta_ln_z'],
        endpoint=end, fractional_time_change=float(reference[3]/reference[0]),
        fractional_phase_change_at_same_radius=float(reference[4]/reference[1]),
        fractional_final_e_change_at_same_radius=float(np.expm1(reference[5]/2)),
        final_e_BH=float(initial_e*end['e_over_initial_BH']), final_e_body=float(initial_e*end['e_over_initial_body']),
        equal_time=dict(scaled_time=time_body, body_separation=5., BH_separation=hole_same_time_radius,
                        scaled_orbital_phase_difference=float(equal_time_phase),
                        first_order_scaled_phase_difference=float(first_order_equal_time_phase),
                        remainder_relative=float(abs(equal_time_phase/first_order_equal_time_phase-1))),
        weak_field_baseline=weak_baseline.tolist(), leading_tidal_minus_horizon_difference=weak_difference.tolist(),
        finite_radius_corrections_to_weak_difference=(reference[3:]/weak_difference-1).tolist(),
        reference_BH_over_Newtonian=(reference[:3]/weak_baseline).tolist(),
        adiabat_maxima=maxima, mass_ratio_for_all_listed_drift_indicators_below_001=float(sufficient_eta_for_indicator001),
        pole_memory_time=1/decay, initial_history_assumption='Retarded adiabatic preparation, no arbitrary free ringing.',
        memory_scope='Known-pole and slow-orbit diagnostics, not a full-response memory error bound or classification of every mode.')
    directory = ROOT/'results/analysis'
    directory.mkdir(parents=True, exist_ok=False)
    result = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(), script_sha256=digest(__file__),
                  input_hashes={**inputs, **imported_hashes()}, summary=summary, endpoint_integrals=final,
                  comparisons=comparisons, independent_gauss_point_controls=gauss_point_controls,
                  ode_control=dict(relative_errors=abs((ode_final-reference)/reference).tolist(), evaluations=ode.nfev),
                  interpolation={label: curve.export() for label, curve in curves.items()}, raw_nodes=nodes,
                  trajectory=trajectory, adiabatic_diagnostics=diagnostics)
    write_json(directory/'status.json', result, exclusive=True)
    write_csv(directory/'trajectory.csv', trajectory)
    write_csv(directory/'adiabatic_diagnostics.csv', diagnostics)
    write_csv(directory/'independent_gauss_point_controls.csv', gauss_point_controls)
    for label, rows in nodes.items():
        write_csv(directory/(label+'-rates.csv'), rows)
    print(dict(summary=summary, comparisons=comparisons, ode_relative_error=result['ode_control']['relative_errors']), flush=True)


if __name__ == '__main__':
    main()

