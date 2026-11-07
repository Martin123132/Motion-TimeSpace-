from __future__ import annotations

from native_common import *


def main():
    modest()
    folder = ROOT / 'results/pressure-projection'
    folder.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'runs/final-bg8-start/heavy.npz'
    data = np.load(source)
    table = np.load(ROOT / 'runs/backgrounds/heavy.npz')
    names = data['names'].tolist()
    scales = data['values'][0, :, names.index('a')]
    phase_of_n = interpolate.CubicSpline(table['heavy_efold'], table['phase_h'])
    phase = phase_of_n(np.log(scales))
    phi = interpolate.CubicSpline(table['heavy_efold'], table['phi_h'])(np.log(scales))
    velocity = interpolate.CubicSpline(table['heavy_efold'], table['phidot_h'])(np.log(scales))
    mass = float(table['heavy_mass_mpc'])
    density = (velocity**2 + (scales*mass*phi)**2)/2
    rows = []
    for center in [.0002, .000225, .00025]:
        center_phase = float(phase_of_n(math.log(center)))
        for width in [4., 6., 8.]:
            chosen = abs(phase-center_phase) < width*math.pi
            coordinate = (phase[chosen]-center_phase)/(width*math.pi)
            for secular_degree, harmonic_degree in [(4, 2), (6, 4), (8, 6)]:
                basis = np.column_stack([coordinate**degree for degree in range(secular_degree+1)] +
                    [coordinate**degree*trig(2*phase[chosen]) for degree in range(harmonic_degree+1)
                        for trig in [np.cos, np.sin]] +
                    [coordinate**degree*trig(4*phase[chosen]) for degree in range(3) for trig in [np.cos, np.sin]])

                def average(values):
                    return float(np.linalg.lstsq(basis, np.asarray(values)[chosen], rcond=None)[0][0])

                abundance = average(scales*density)
                for index, mode in enumerate(data['modes']):
                    values = data['values'][index]
                    hubble = values[:, names.index('H')]
                    delta = average(scales*values[:, names.index('mts_drho_h')])/abundance
                    pressure = average(scales*values[:, names.index('mts_dp_h')])/abundance
                    momentum = average(scales*mode*values[:, names.index('mts_q_h')]/hubble)/abundance
                    center_hubble = average(hubble)
                    ratio = (mode/(center*mass))**2
                    sound2 = ratio/(math.sqrt(1+ratio)+1)**2
                    closure = sound2*(delta+3*momentum*(center_hubble/mode)**2)
                    norm = max(abs(delta), abs(momentum)/max(1.,mode/center_hubble*math.sqrt(sound2)), 1e-6)
                    rows.append(dict(center_a=center, k_Mpc_inverse=float(mode), width_pi=width,
                        secular_degree=secular_degree, harmonic_degree=harmonic_degree,
                        heavy_delta=delta, heavy_velocity=momentum, heavy_pressure=pressure,
                        pressure_prediction=closure, mismatch_over_mode_norm=abs(pressure-closure)/norm,
                        matrix_condition_number=float(np.linalg.cond(basis))))
    groups = []
    for width in [4., 6., 8.]:
        for degree in [4, 6, 8]:
            chosen = [row for row in rows if row['width_pi']==width and row['secular_degree']==degree]
            groups.append(dict(width_pi=width, secular_degree=degree,
                maximum_pressure_mismatch=max(row['mismatch_over_mode_norm'] for row in chosen),
                maximum_condition=max(row['matrix_condition_number'] for row in chosen)))
    finish(folder, dict(rows=rows, summaries=groups, scope='Projection-order and window sensitivity, not a new physical fit'),
        __file__, [source, ROOT / 'runs/backgrounds/heavy.npz'])
    print(json.dumps(groups, indent=2), flush=True)


if __name__ == '__main__':
    main()
