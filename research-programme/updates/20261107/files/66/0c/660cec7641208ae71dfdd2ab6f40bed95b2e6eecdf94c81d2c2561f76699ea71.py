from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp
from scipy.special import beta as beta_function

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'surface-susceptibility-20261006'
sys.path.insert(0, str(PARENT))
from susceptibility import digest, read_json, write_json, modest_process
sys.path.insert(0, str(BRANCH/'retarded-response-20261004'))
from response_system_v2 import potential, asymptotic_coefficients


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.update([PARENT/'results/stage-integrity.json',
                  PARENT/'results/tangent/status.json',
                  PARENT/'results/validation/status.json'])
    return {str(path):digest(path) for path in sorted(paths)}


def save(directory, script, report):
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def body():
    parent = read_json(PARENT/'results/tangent/status.json')
    refined = next(row for row in parent['rows'] if row['label'] == 'refined')
    radius, mass = parent['radius'], parent['mass']
    return dict(radius=radius, mass=mass, compactness=mass/radius,
                inertia=-refined['coefficient_s2']/radius,
                stiffness=refined['static_slope']*radius,
                coefficient_s2=refined['coefficient_s2'])


def coordinate(position, compactness):
    return position-1+2*compactness*np.log((position-2*compactness)/(1-2*compactness))


def spatial_rule(count, compactness, detector):
    positions, weights = [], []
    knots = [1., 5., 20., 80., detector]
    nodes, base_weights = leggauss(count)
    for left, right in zip(knots[:-1], knots[1:]):
        values = (left+right)/2+(right-left)*nodes/2
        positions.extend(values)
        weights.extend((right-left)*base_weights/2/(1-2*compactness/values))
    return np.asarray(positions), np.asarray(weights)


def spectrum(count):
    nodes, weights = leggauss(count)
    center, width = .018, .012
    frequencies = center+width*nodes
    amplitudes = (1-nodes**2)**8/(width*beta_function(.5, 9))
    return frequencies, width*weights, amplitudes


def transfer(frequency, positions, model, far_phase=40., order=10, tolerance=2e-11):
    mass = model['compactness']
    surface_slope = model['stiffness']-model['inertia']*frequency**2
    detector = float(max(positions))
    outer = max(1.1*detector, far_phase/frequency)
    coefficients = asymptotic_coefficients(mass*frequency, order)
    indices = np.arange(order+1)
    argument = frequency*outer
    series = np.sum(coefficients*argument**(-indices))
    series_prime = np.sum(-indices*coefficients*argument**(-indices-1))
    phase = np.exp(1j*frequency*coordinate(outer, mass))
    initial = phase*np.array([series, 1j*frequency*series+(1-2*mass/outer)*frequency*series_prime])

    def equation(position, state):
        return np.array([state[1], (potential(position, mass)-frequency**2)*state[0]])/(1-2*mass/position)

    inward = solve_ivp(equation, (outer, 1.), initial, method='DOP853',
                       rtol=tolerance, atol=tolerance/100, dense_output=True)
    assert inward.success, inward.message
    outward = solve_ivp(equation, (1., detector), np.array([0., 1.]), method='DOP853',
                        rtol=tolerance, atol=tolerance/100, dense_output=True)
    assert outward.success, outward.message
    outgoing_surface = inward.sol(1.)
    normalization = outgoing_surface[0]
    real_slope = float((outgoing_surface[1]/normalization).real)
    current = float(np.imag(np.conj(initial[0])*initial[1]))
    beta = current/abs(normalization)**2
    difference = real_slope-surface_slope
    denominator = difference**2+beta**2
    outgoing = inward.sol(positions)/normalization
    standing = outgoing.real
    dirichlet = outward.sol(positions)
    regular = standing-difference*dirichlet
    source_index = int(np.flatnonzero(positions == 5.)[0])
    source_regular = regular[0, source_index]
    source_standing, source_dirichlet = standing[0, source_index], dirichlet[0, source_index]
    inner = positions <= 5.
    real_green = np.where(inner[None, :],
        -regular*(difference*source_standing+beta**2*source_dirichlet)/denominator,
        -source_regular*(difference*standing+beta**2*dirichlet)/denominator)
    imaginary_green = beta*source_regular*regular/denominator
    green = real_green+1j*imaginary_green
    infinity = -source_regular/(normalization*complex(difference, beta))
    direct_outgoing = -source_regular*outgoing/complex(difference, beta)
    jump = -source_regular*(difference*standing[1, source_index]+beta**2*dirichlet[1, source_index])/denominator
    jump -= -regular[1, source_index]*(difference*source_standing+beta**2*source_dirichlet)/denominator
    raw_current = np.imag(np.conj(inward.sol(detector)[0])*inward.sol(detector)[1])
    controls = dict(derivative_jump_error=abs(jump+1),
        surface_boundary_error=abs(green[1, 0]-surface_slope*green[0, 0])/max(abs(green[0, 0]), 1e-300),
        outgoing_series_current_error=abs(current/frequency-1),
        raw_detector_current_error=abs(raw_current/current-1),
        outgoing_reconstruction_error=float(np.max(abs(green[:, ~inner]-direct_outgoing[:, ~inner]))/
                                              max(float(np.max(abs(green[:, ~inner]))), 1e-300)),
        optical_error=abs(green[0, source_index].imag-current*abs(infinity)**2)/
                      max(current*abs(infinity)**2, 1e-300),
        detector_optical_error=abs(np.imag(np.conj(green[0, -1])*green[1, -1])-current*abs(infinity)**2)/
                               max(current*abs(infinity)**2, 1e-300),
        nfev=inward.nfev+outward.nfev)
    return green, infinity, controls


def synthesize(time, frequencies, weights, amplitudes, responses, derivative=0):
    factors = weights*amplitudes*(-1j*frequencies)**derivative
    return np.real(np.exp(-1j*np.outer(time, frequencies))@(factors[:, None]*responses))


def energy_series(time, archive):
    frequencies, weights, amplitudes = (archive[key] for key in ['frequencies', 'frequency_weights', 'amplitudes'])
    green = archive['green']
    wave = synthesize(time, frequencies, weights, amplitudes, green[:, 0])
    velocity = synthesize(time, frequencies, weights, amplitudes, green[:, 0], 1)
    acceleration = synthesize(time, frequencies, weights, amplitudes, green[:, 0], 2)
    slope = synthesize(time, frequencies, weights, amplitudes, green[:, 1])
    slope_velocity = synthesize(time, frequencies, weights, amplitudes, green[:, 1], 1)
    source = synthesize(time, frequencies, weights, amplitudes, np.ones((len(frequencies), 1)))[:, 0]
    source_index = int(archive['source_index'])
    positions, spatial_weights = archive['positions'], archive['spatial_weights']
    interior = archive['energy_indices'].astype(int)
    potential_values = potential(positions[interior], float(archive['compactness']))
    density = velocity[:, interior]**2+slope[:, interior]**2+potential_values*wave[:, interior]**2
    bulk = .5*density@spatial_weights
    bulk_rate = (velocity[:, interior]*acceleration[:, interior]
                 +slope[:, interior]*slope_velocity[:, interior]
                 +potential_values*wave[:, interior]*velocity[:, interior])@spatial_weights
    inertia, stiffness = float(archive['inertia']), float(archive['stiffness'])
    surface_kinetic = .5*inertia*velocity[:, 0]**2
    surface_potential = .5*stiffness*wave[:, 0]**2
    surface = surface_kinetic+surface_potential
    surface_rate = inertia*velocity[:, 0]*acceleration[:, 0]+stiffness*wave[:, 0]*velocity[:, 0]
    work = source*velocity[:, source_index]
    flux = -velocity[:, -1]*slope[:, -1]
    infinity_velocity = synthesize(time, frequencies, weights, amplitudes, archive['infinity'][:, None], 1)[:, 0]
    radiation = infinity_velocity**2
    return dict(time=time, source=source, bulk=bulk, surface=surface,
                surface_kinetic=surface_kinetic, surface_potential=surface_potential,
                bulk_rate=bulk_rate, surface_rate=surface_rate, work=work, flux=flux,
                radiation=radiation, boundary_velocity=velocity[:, 0], boundary_slope=slope[:, 0])

