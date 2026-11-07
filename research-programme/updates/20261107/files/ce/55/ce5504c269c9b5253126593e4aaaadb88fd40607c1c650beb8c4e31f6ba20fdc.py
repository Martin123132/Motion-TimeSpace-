from __future__ import annotations

from matching_common import *


def project(data, table, center, density0, width, degree):
    names = data['names'].tolist()
    values = data['values']
    scales = values[0, :, names.index('a')]
    phase_spline = interpolate.CubicSpline(table['heavy_efold'], table['phase_h'])
    phase = phase_spline(np.log(scales))
    central_phase = float(phase_spline(math.log(center)))
    chosen = abs(phase-central_phase) < width*math.pi
    coordinate = (phase[chosen]-central_phase)/(width*math.pi)
    basis = np.column_stack([coordinate**power for power in range(degree+1)] +
        [coordinate**power*trig(2*phase[chosen]) for power in range(degree-1)
            for trig in [np.cos, np.sin]] +
        [coordinate**power*trig(4*phase[chosen]) for power in range(3) for trig in [np.cos, np.sin]])

    def average(series):
        return float(np.linalg.lstsq(basis, np.asarray(series)[chosen], rcond=None)[0][0])

    rows = []
    for mode, value in zip(data['modes'], values):
        density = average(scales*value[:, names.index('mts_drho_h')])/density0
        momentum = average(scales*value[:, names.index('mts_q_h')])/density0
        pressure = average(scales*value[:, names.index('mts_dp_h')])/density0
        hubble = average(value[:, names.index('H')])
        ratio = (mode/(center*float(table['heavy_mass_mpc'])))**2
        sound2 = ratio/(math.sqrt(1+ratio)+1)**2
        predicted = sound2*(density+3*hubble*momentum/mode)
        norm = max(abs(density), abs(mode*momentum/hubble)/max(1., mode/hubble*math.sqrt(sound2)), 1e-6)
        rows.append(dict(k=float(mode), delta=density, momentum=momentum, pressure=pressure,
            closure_pressure=predicted, pressure_error_over_mode_norm=abs(pressure-predicted)/norm,
            mode_norm=norm, mass_over_H=center*float(table['heavy_mass_mpc'])/hubble))
    return rows, dict(points=int(chosen.sum()), condition=float(np.linalg.cond(basis)), width_pi=width, degree=degree)


def main():
    modest()
    folder = ROOT / 'runs/matching-inputs'
    folder.mkdir(parents=True, exist_ok=False)
    table = np.load(BACKGROUND)
    data = np.load(REFERENCE)
    omega_m, slow_mass = previous.inherited_parameters()
    fraction = float(table['fraction'])
    unit = previous.H0/previous.C_LIGHT
    density0 = 3*unit**2*fraction*omega_m
    mass = float(table['heavy_mass_mpc'])
    phi = interpolate.CubicSpline(table['heavy_efold'], table['phi_h'])
    phidot = interpolate.CubicSpline(table['heavy_efold'], table['phidot_h'])
    phase = interpolate.CubicSpline(table['heavy_efold'], table['phase_h'])
    inverse_phase = interpolate.PchipInterpolator(table['phase_h'], table['heavy_efold'])

    def residual(efold):
        scale = np.exp(efold)
        return scale*(phidot(efold)**2+(scale*mass*phi(efold))**2)/(2*density0)-1

    species = previous.StandardSpecies(omega_m, fraction)
    reports = []
    for nominal in [.0002, .000225, .00025]:
        midpoint = float(phase(math.log(nominal)))
        trial = inverse_phase(midpoint+np.linspace(-2*math.pi, 2*math.pi, 201))
        crossings = np.flatnonzero(residual(trial[:-1])*residual(trial[1:]) < 0)
        roots = [optimize.brentq(residual, trial[index], trial[index+1], xtol=2e-14) for index in crossings]
        match_n = min(roots, key=lambda value: abs(value-math.log(nominal)))
        match_a = math.exp(match_n)

        def heavy_density(efold):
            nodes = np.asarray(efold)
            exact_nodes = np.minimum(nodes, match_n)
            scale = np.exp(exact_nodes)
            velocity = phidot(exact_nodes)
            rho = (velocity**2+(scale*mass*phi(exact_nodes))**2)/(6*unit**2*scale**2)
            rho_n = -velocity**2/(unit**2*scale**2)
            dust = fraction*omega_m*np.exp(-3*nodes)
            return np.where(nodes < match_n, rho, dust), np.where(nodes < match_n, rho_n, -3*dust)

        initial, slow, flatness = previous.solve_slow(species, heavy_density, slow_mass)
        nodes = np.unique(np.concatenate([table['efold'], [match_n]]))
        scales = np.exp(nodes)
        field, velocity = slow.sol(nodes)
        rho, rho_n = heavy_density(nodes)
        expansion2 = (species.values(nodes)[0]+rho+slow_mass**2*field**2)/(1-velocity**2)
        base = {key: table[key] for key in ['heavy_efold', 'phi_h', 'phidot_h', 'phase_h',
            'slow_mass_mpc', 'heavy_mass_mpc', 'fraction']}
        base.update(efold=nodes, scale=scales, phi_s=math.sqrt(6)*field,
            phidot_s=math.sqrt(6)*scales*unit*np.sqrt(expansion2)*velocity,
            heavy_logrho_mpc=np.log(3*unit**2*rho), heavy_w=-1-rho_n/(3*rho),
            expansion2=expansion2, matching_scale=match_a, matching_density=density0, modes=MODES)
        projections = []
        for width, degree in [(6, 8), (4, 8), (6, 6), (4, 6)]:
            rows, details = project(data, table, match_a, density0, width, degree)
            tag = f'a{round(nominal*1e6):03d}-w{width}-d{degree}'
            path = folder / (tag + '.npz')
            np.savez_compressed(path, **base, matching_delta=[row['delta'] for row in rows],
                matching_momentum=[row['momentum'] for row in rows])
            projections.append(dict(tag=tag, rows=rows, **details))
        reports.append(dict(nominal_a=nominal, matching_a=match_a, phase_displacement=float(phase(match_n))-midpoint,
            background_density_jump_fraction=abs(residual(match_n)), slow_initial=initial,
            flatness_error=abs(flatness-1), projections=projections))
        print('Prepared', nominal, 'continuous-density switch at', match_a, flush=True)
    finish(folder, dict(matches=reports, matching_uses_source_projection=True, mode_interpolation=False,
        standard_species_phase_averaged=False, slow_background_reintegrated=True), __file__,
        [BACKGROUND, REFERENCE, *native_hashes(), *folder.glob('*.npz')])


if __name__ == '__main__':
    main()
