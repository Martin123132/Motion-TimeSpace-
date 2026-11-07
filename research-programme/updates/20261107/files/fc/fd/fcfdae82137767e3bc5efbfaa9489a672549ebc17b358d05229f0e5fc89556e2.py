from common import *
from metric_channels import derive
import numpy as np
import sympy as sp


def symbolic():
    speed, epsilon, eta, density = sp.symbols('v epsilon eta d', positive=True)
    width = sp.sqrt(speed**2 + 4 * epsilon**2)
    width_rate = (-speed**2 * (1 - speed**2) + 4 * epsilon**2 * eta) / width**2
    lower = speed**2 / (sp.sqrt(3) * epsilon * width)
    upper = -width / (sp.sqrt(3) * epsilon)
    checks = dict(streaming_symmetric=sp.simplify((upper + lower) / 2 + 2 * epsilon / (sp.sqrt(3) * width)),
                  width_derivative=sp.simplify((-speed * (1 - speed**2) * sp.diff(width, speed) + eta * epsilon * sp.diff(width, epsilon)) / width - width_rate),
                  no_inverse_speed_force=sp.simplify(speed * sp.sqrt(3 * density) / 2 * 4 / (3 * epsilon * speed) - 2 * sp.sqrt(density) / (sp.sqrt(3) * epsilon)),
                  cold_stream_upper=sp.simplify(upper.subs(speed, 0) + 2 / sp.sqrt(3)),
                  cold_stream_lower=sp.simplify(lower.subs(speed, 0)),
                  cold_weight_rate=sp.simplify((-(1 + speed**2) / 2 + width_rate).subs(speed, 0) - eta + sp.Rational(1, 2)))
    wave, hubble, hubble_n, quadrature, defect, enthalpy = sp.symbols('k H HN Wq DeltaW W', real=True, nonzero=True)
    free_d, free_q, current, psi = sp.symbols('ld lq Q Psi', real=True)
    phi_n = -(free_d + 3 * (hubble_n * current + hubble * free_q) / wave + 3 * quadrature * psi) / (2 * wave**2 + 3 * quadrature)
    direct = -((free_d + 3 * defect * psi + 3 * quadrature * phi_n) / (2 * wave**2)
               + 3 * (hubble_n * current + hubble * free_q + enthalpy * wave * psi) / (2 * wave**3))
    checks['gr_phi_derivative'] = sp.factor((direct - phi_n).subs(enthalpy, quadrature - defect))
    alpha, defect_n, alpha_n = sp.symbols('alpha DWN alphaN', real=True)
    correction_rate = -wave * (defect_n * alpha - defect * alpha)
    checks['thermal_defect_current'] = sp.expand(correction_rate - 2 * wave * defect * alpha + wave * (defect_n + defect) * alpha)
    require(all(value == 0 for value in checks.values()), 'exact cold/GR identities')
    return {name: str(value) for name, value in checks.items()}


def coefficients(epsilon, speed, eta):
    epsilon, speed = np.asarray(epsilon), np.asarray(speed)
    width = np.hypot(speed, 2 * epsilon)
    width_rate = (-speed**2 * (1 - speed**2) + 4 * epsilon**2 * eta) / width**2
    diagonal0 = -(1 + speed**2) / 2 + width_rate
    diagonal1 = -(3 - speed**2) / 2
    symmetric = -2 * epsilon / (np.sqrt(3) * width)
    logarithmic = .5 * (diagonal0 + diagonal1 + np.hypot(diagonal0 - diagonal1, 2 * symmetric))
    simple_bound = np.maximum(eta - .5, -1) + 1 / np.sqrt(3)
    return width, width_rate, diagonal0, diagonal1, symmetric, logarithmic, simple_bound


def adapt(system, energy, efold):
    old = derive(system, energy, efold)
    point = system.context['point'](efold)
    hubble = old['hubble']
    eta = float(system.background_spline(efold, 1)[0] / hubble)
    epsilon = hubble / system.wave
    speeds = system.context['kinetic'](point[11])[1]
    massive = np.array(energy.massive_origin) * (energy.origin_scale / point[10])**2 * energy.speeds_origin / speeds
    width, width_rate, diagonal0, diagonal1, symmetric, logarithmic, simple = coefficients(epsilon, speeds, eta)
    scaling, scaling_rate = np.ones(energy.size), np.zeros(energy.size)
    for node in range(5):
        scaling[energy.moment_slot(0, node)] = width[node]
        scaling_rate[energy.moment_slot(0, node)] = width_rate[node]
        for degree in (1, 2):
            scaling[energy.moment_slot(degree, node)] = speeds[node]
            scaling_rate[energy.moment_slot(degree, node)] = -(1 - speeds[node]**2)
    rows = {name: old[name] / scaling for name in ('density', 'current', 'shear', 'free_density', 'psi', 'phi_rate')}
    rows['density_rate'] = old['density_rate'] / scaling - rows['density'] * scaling_rate
    rows['psi_injection'] = scaling * old['psi_injection']
    rows['phi_injection'] = scaling * old['phi_injection']
    rows['transform'] = scaling[:, None] * old['transform']
    rows['inverse'] = old['inverse'] / scaling[None, :]
    rows['derivative'] = scaling[:, None] * old['derivative'] / scaling[None, :] + np.diag(scaling_rate)
    direct_massive = []
    for node in range(5):
        root = np.sqrt(massive[node])
        slots = [energy.moment_slot(degree, node) for degree in range(3)]
        direct_massive.append(dict(slots=slots, density0=2 * root / width[node],
                                   density0_rate=2 * root / width[node] * (-(1 + speeds[node]**2) / 2 - width_rate[node]),
                                   free0=-2 * (1 + speeds[node]**2) * root / width[node],
                                   free1=-2 * root / (np.sqrt(3) * epsilon),
                                   current1=2 * root / np.sqrt(3), shear2=2 * root * speeds[node] / np.sqrt(5),
                                   psi1=2 * root / (np.sqrt(3) * epsilon), phi0=2 * root * width[node]))
    return dict(old=old, rows=rows, scaling=scaling, scaling_rate=scaling_rate, epsilon=epsilon, eta=eta,
                speeds=speeds, massive=massive, width=width, width_rate=width_rate,
                diagonal0=diagonal0, diagonal1=diagonal1, symmetric=symmetric,
                massive_logarithmic=logarithmic, simple_bound=float(simple), direct_massive=direct_massive,
                tail_weights=energy.tail_weights * speeds, tail_rate=diagonal1)


def pressure_and_current(system, energy, efold, adapted):
    rows, old = adapted['rows'], adapted['old']
    point = system.context['point'](efold)
    hubble, wave = old['hubble'], system.wave
    weights = np.diag(rows['transform']) / system.units[:energy.size]
    density = energy.fluid_origin * (energy.origin_scale / point[10])**np.array([1., 1., 2., 2.])
    baryon = energy.slot(4)
    native_pressure = np.zeros(energy.size)
    for column in range(energy.size):
        state = np.zeros(len(system.units))
        state[:energy.size] = rows['inverse'][:, column] * system.units[:energy.size]
        raw = system.decode(efold, state)
        native_pressure[column] = weights[baryon] * wave / hubble * system.context['observe'](point[11], system.project(raw))[18]
    pressure = native_pressure * np.sqrt(density[1]) * hubble / wave
    current_rate = np.zeros(energy.size)
    alpha = system.alpha_slot
    current_rate[alpha] = (-density[0] - old['defect_rate']) / np.sqrt(density[0]) + .5 * rows['current'][alpha]
    current_rate[baryon] = -.5 * rows['current'][baryon]
    signature = system.context['signature_values']
    for species, beginning in ((2, int(signature[3])), (3, int(signature[4]))):
        monopole, dipole = energy.slot(beginning), energy.slot(beginning + 1)
        pressure[monopole] += density[species] / (3 * weights[monopole])
        current_rate[dipole] = -rows['current'][dipole]
    for node in range(5):
        monopole, dipole = energy.moment_slot(0, node), energy.moment_slot(1, node)
        pressure[monopole] += 2 * np.sqrt(adapted['massive'][node]) * adapted['speeds'][node]**2 / (3 * adapted['width'][node])
        current_rate[dipole] = -(1 + adapted['speeds'][node]**2) / 2 * rows['current'][dipole]
    for scalar in old['scalars']:
        slots = scalar['slots']
        omega, full = scalar['omega'], scalar['full_frequency']
        pressure[slots] = [-omega**2 * scalar['field'] / full, scalar['velocity']]
        current_rate[slots[0]] = wave / full * (point[2 * scalar['species'] + 6] - omega**2 / full**2 * scalar['velocity'])
    free_current = -2 * rows['current'] + wave / hubble * (pressure - 2 / 3 * rows['shear'])
    free_current[alpha] -= (old['defect_rate'] + old['defect']) / np.sqrt(density[0])
    gr_psi = -rows['density'] / (2 * wave**2) - 3 * hubble * rows['current'] / (2 * wave**3) - rows['shear'] / wave**2
    gr_phi = -rows['density'] / (2 * wave**2) - 3 * hubble * rows['current'] / (2 * wave**3)
    hubble_n = hubble * adapted['eta']
    gr_phi_rate = -(rows['free_density'] + 3 * (hubble_n * rows['current'] + hubble * free_current) / wave + 3 * old['quadrature'] * gr_psi) / old['denominator']
    return dict(native_pressure=native_pressure, pressure=pressure, current_rate=current_rate,
                free_current=free_current, gr_psi=gr_psi, gr_phi=gr_phi, gr_phi_rate=gr_phi_rate,
                density_weights=density)


def comparison(system, energy, adapted, physical, matrix, branch):
    rows, old = adapted['rows'], adapted['old']
    selected_psi = physical['gr_psi'] if branch == 'gr' else rows['psi']
    selected_phi = physical['gr_phi_rate'] if branch == 'gr' else rows['phi_rate']
    rest, heavy = energy.rest, energy.heavy
    signature = system.context['signature_values']
    hubble = old['hubble']
    weights = np.diag(rows['transform']) / system.units[:energy.size]
    ufa = 0.
    if signature[12]:
        quad = energy.slot(int(signature[4]) + 2)
        ufa = -4 * weights[quad] * hubble * (adapted['eta'] - 1) / weights[system.alpha_slot]
    fluid_mu = .5 * (adapted['eta'] - 2 + np.sqrt((adapted['eta'] + 1)**2 + 1))
    slow = old['scalars'][0]
    base = max(0., fluid_mu, slow['omega']**2 / slow['full_frequency']**2, float(np.max(adapted['massive_logarithmic'])))
    free_bound = base + np.linalg.norm(physical['native_pressure'][rest]) + abs(ufa) / 2
    def coupling(destination, origin):
        return (np.linalg.norm(rows['psi_injection'][destination]) * np.linalg.norm(selected_psi[origin])
                + np.linalg.norm(rows['phi_injection'][destination]) * np.linalg.norm(selected_phi[origin]))
    tail = float(np.max(adapted['tail_rate']))
    actual_rest = max(tail, float(np.linalg.eigvalsh((matrix[np.ix_(rest, rest)] + matrix[np.ix_(rest, rest)].T) / 2)[-1]))
    result = np.zeros((2, 2))
    actual = np.zeros((2, 2))
    result[1, 1] = free_bound + coupling(rest, rest)
    actual[1, 1] = actual_rest
    rescaling = np.ones(energy.size)
    if len(heavy):
        scalar = old['scalars'][1]
        balance = system.wave / scalar['full_frequency']
        rescaling[heavy] = balance
        result[0, 0] = coupling(heavy, heavy)
        result[0, 1] = balance * coupling(heavy, rest)
        result[1, 0] = coupling(rest, heavy) / balance
        actual[0, 0] = float(np.linalg.eigvalsh((matrix[np.ix_(heavy, heavy)] + matrix[np.ix_(heavy, heavy)].T) / 2)[-1]) - scalar['omega']**2 / scalar['full_frequency']**2
        actual[0, 1] = balance * np.linalg.norm(matrix[np.ix_(heavy, rest)], ord=2)
        actual[1, 0] = np.linalg.norm(matrix[np.ix_(rest, heavy)], ord=2) / balance
    return dict(actual=actual, upper=result, base=base, free_bound=free_bound, ufa=ufa, rescaling=rescaling)
