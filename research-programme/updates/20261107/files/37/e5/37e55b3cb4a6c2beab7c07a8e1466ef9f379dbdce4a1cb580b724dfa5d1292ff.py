from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial import Chebyshev

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'matched-inspiral-20261006'
CLOCK = BRANCH/'postcircular-clock-20261005'
sys.path.insert(0, str(CLOCK))
from carrier import digest, read_json, write_json, modest_process, orbit_series
from sidebands import polar_vacuum
from secular import geometry


def save(name, script, report):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    return {str(path):digest(path) for path in sorted(paths)}


def number(row, key):
    return complex(*row[key])


def pair(value):
    return [float(value.real), float(value.imag)]


def frozen_boundary(row, archive, static_slope):
    alpha = float(archive['real_outgoing'][0, 1])
    slope = float(archive['direct_body'][0, 1])
    frequency = float(row['frequency'])
    sources = np.array(row['source_coefficients'])
    real_source = sources@archive['real_outgoing'][-1]
    dirichlet_source = sources@archive['dirichlet'][-1]
    direct_source = real_source+(slope-alpha)*dirichlet_source
    reference = number(row['responses'][0], 'reference_amplitude')
    change = number(row['responses'][0], 'delta_amplitude')
    amplitude = reference+change
    current = frequency*abs(amplitude)**2/direct_source[0]**2
    discriminant = 1-4*current**2*(alpha-slope)**2
    assert discriminant > 0
    beta = 2*current*(alpha-slope)**2/(1+np.sqrt(discriminant))
    wronskian = complex(alpha-slope, beta)
    frozen_wronskian = complex(alpha-static_slope, beta)
    normalization = direct_source[0]/(wronskian*amplitude)
    sigma = static_slope-slope
    result = []
    errors = []
    for index, response in enumerate(row['responses']):
        overlap = complex(real_source[index], beta*dirichlet_source[index])
        amplitude_change = sigma*overlap/(wronskian*frozen_wronskian*normalization)
        frozen_change = number(response, 'delta_amplitude')+amplitude_change
        action = -3/(8*np.pi)*frozen_change*normalization*overlap
        frozen_direct = (real_source[index]+(static_slope-alpha)*dirichlet_source[index])/(frozen_wronskian*normalization)
        frozen_total = number(response, 'reference_amplitude')+frozen_change
        power = 3*frequency**2/(4*np.pi)*(2*(number(response, 'reference_amplitude').conjugate()*frozen_change).real+abs(frozen_change)**2)
        horizon_power = 3*frequency**2/(4*np.pi)*abs(number(response, 'horizon_amplitude'))**2
        errors.append(dict(reconstruction=abs(frozen_direct-frozen_total)/max(abs(frozen_total), 1e-300),
            optical=abs(2*frequency*action.imag-power+horizon_power)/max(abs(power)+horizon_power, 1e-300)))
        result.append({**response, 'delta_amplitude':pair(frozen_change),
            'difference_coefficient':pair(frozen_change*normalization), 'outgoing_source':pair(overlap), 'action':pair(action)})
    if 'outgoing_source' in row['responses'][0]:
        known = number(row['responses'][0], 'outgoing_source')
        beta_error = abs(beta/(known.imag/dirichlet_source[0])-1)
    else:
        beta_error = None
    diagnostic = dict(frequency=frequency, separation=row.get('separation'), slope=slope, static_slope=static_slope,
        recovered_beta=beta, current_beta_relative_error=beta_error, small_current_branch=abs(beta/(alpha-slope)),
        maximum_direct_error=max(value['reconstruction'] for value in errors),
        maximum_optical_error=max(value['optical'] for value in errors))
    return {**row, 'responses':result}, diagnostic


def carrier_flux(rows, step=.0005):
    lookup = {row['fractional_frequency_shift']:row for row in rows}
    center = lookup[0.]
    alpha = orbit_series(center['semilatus'])['angular_frequency_fraction']
    factor = 3*center['frequency']**2/(4*np.pi)
    leading, second = {}, {}
    for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude', 'action']:
        leading[key] = number(center['responses'][0], key)
        derivative = sum(weight*number(lookup[shift*step]['responses'][0], key)
            for shift, weight in [(-2, 1), (-1, -8), (1, 8), (2, -1)])/(12*step)
        second[key] = number(center['responses'][1], key)+alpha*derivative
    reference, difference, horizon = [leading[key] for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']]
    reference2, difference2, horizon2 = [second[key] for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']]
    output = dict(reference=[factor*abs(reference)**2, 2*factor*((reference.conjugate()*reference2).real+alpha*abs(reference)**2)],
        horizon=[factor*abs(horizon)**2, 2*factor*((horizon.conjugate()*horizon2).real+alpha*abs(horizon)**2)],
        difference=[factor*(2*(reference.conjugate()*difference).real+abs(difference)**2),
            2*factor*((reference2.conjugate()*difference+reference.conjugate()*difference2+difference.conjugate()*difference2).real
                      +alpha*(2*(reference.conjugate()*difference).real+abs(difference)**2))])
    output['nonlinear_difference'] = [factor*abs(difference)**2,
        2*factor*((difference.conjugate()*difference2).real+alpha*abs(difference)**2)]
    center_action2 = -3/(8*np.pi)*(number(center['responses'][1], 'difference_coefficient')*number(center['responses'][0], 'outgoing_source')
        +number(center['responses'][0], 'difference_coefficient')*number(center['responses'][1], 'outgoing_source'))
    derivative_action = sum(weight*number(lookup[shift*step]['responses'][0], 'action')
        for shift, weight in [(-2, 1), (-1, -8), (1, 8), (2, -1)])/(12*step)
    output['action'] = [leading['action'].real, (center_action2+alpha*derivative_action).real]
    return output


def sideband_response(row):
    reference, change, horizon = [complex(row[key+'_real'], row[key+'_imag'])
                                 for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']]
    return dict(frequency=row['frequency'], separation=row['separation_over_radius'], semilatus=row['semilatus'],
        source_coefficients=[[row['master_coefficient'], row['slope_coefficient']]],
        responses=[dict(reference_amplitude=pair(reference), delta_amplitude=pair(change),
            horizon_amplitude=pair(horizon))])


def sideband_flux(row):
    response = row['responses'][0]
    reference, difference, horizon = [number(response, key) for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']]
    factor = 3*row['frequency']**2/(4*np.pi)
    return dict(reference=factor*abs(reference)**2, horizon=factor*abs(horizon)**2,
        difference=factor*(2*(reference.conjugate()*difference).real+abs(difference)**2),
        nonlinear_difference=factor*abs(difference)**2)


def project_rates(mass, semilatus, circular, sidebands):
    state = geometry(mass, semilatus, 0.)
    coefficient = mass*semilatus**1.5*np.sqrt(semilatus-6)/(2*(semilatus-2)*np.sqrt(semilatus-3))
    derivative_coefficient = coefficient*(1.5/semilatus+.5/(semilatus-6)-1/(semilatus-2)-.5/(semilatus-3))
    angular0 = sum(row['azimuth']*row['power0']/row['frequency'] for row in circular)
    shrink = -angular0/state['angular_p']
    radial = -sum(row['harmonic']*row['power']/row['frequency'] for row in sidebands)
    gamma = (radial-derivative_coefficient*shrink)/coefficient
    angular2 = sum(row['azimuth']*(row['power2']-row['alpha']*row['power0'])/row['frequency'] for row in circular)
    angular2 += sum(row['azimuth']*row['power']/row['frequency'] for row in sidebands)
    energy2 = sum(row['power2'] for row in circular)+sum(row['power'] for row in sidebands)
    angular_z = state['angular']/(2*(semilatus-3))
    angular_cross = -mass*(semilatus+6)/(4*(semilatus-3)**2.5)
    second = (-angular2-angular_cross*shrink-angular_z*gamma)/state['angular_p']
    energy_factor = 1/(2*(semilatus-3))-2/(semilatus-2)**2
    energy_z = state['energy']*energy_factor
    energy_cross = state['energy_p']*energy_factor+state['energy']*(-1/(2*(semilatus-3)**2)+4/(semilatus-2)**3)
    independent = (-energy2-energy_cross*shrink-energy_z*gamma)/state['energy_p']
    return dict(P0=shrink, G0=gamma, P2=second, energy_inverse_P2=independent,
        balance_error=abs(second-independent)/max(abs(second), abs(shrink)*1e-8, 1e-300))


def frequency_geometry(semilatus):
    alpha = orbit_series(semilatus)['angular_frequency_fraction']
    eccentric_map = np.sqrt(semilatus*(semilatus-6))/(semilatus-2)
    log_derivative = .5/semilatus+.5/(semilatus-6)-1/(semilatus-2)
    numerator = semilatus**2-10*semilatus+22
    denominator = (semilatus-6)*(semilatus-2)
    alpha_prime = -1.5*((2*semilatus-10)*denominator-numerator*(2*semilatus-8))/denominator**2
    displacement = -2*semilatus*alpha/3
    displacement_prime = -2*(alpha+semilatus*alpha_prime)/3
    return eccentric_map, log_derivative, displacement, displacement_prime


class RateCurve:
    def __init__(self, rows, component, mass, radius):
        self.mass, self.radius = mass, radius
        self.component = component
        self.nodes = [row for row in rows if row['component'] == component]
        self.power = 3 if component == 'point_out' else 7 if component == 'horizon' else 8
        self.polynomials = {}
        for name, exponent in [('P0', self.power), ('P2', self.power), ('G0', self.power+1)]:
            coordinate = [row['separation'] for row in self.nodes]
            values = [row[name]*(row['semilatus']**exponent)*mass**2 for row in self.nodes]
            self.polynomials[name] = Chebyshev.fit(coordinate, values, len(values)-1, domain=[5., 10.])

    def rates(self, separation):
        semilatus = separation*self.radius/self.mass
        result = {key:float(poly(separation))/(self.mass**2*semilatus**(self.power+(key=='G0')))
                  for key, poly in self.polynomials.items()}
        derivative = (float(self.polynomials['P0'].deriv()(separation))*self.mass/self.radius
                      -self.power*float(self.polynomials['P0'](separation))/semilatus)/(self.mass**2*semilatus**self.power)
        eccentric_map, log_derivative, displacement, displacement_prime = frequency_geometry(semilatus)
        result['X2'] = (result['P2']+displacement_prime*result['P0']+displacement*result['G0']-displacement*derivative)/eccentric_map
        result['G_action'] = result['G0']+log_derivative*result['P0']
        return result
