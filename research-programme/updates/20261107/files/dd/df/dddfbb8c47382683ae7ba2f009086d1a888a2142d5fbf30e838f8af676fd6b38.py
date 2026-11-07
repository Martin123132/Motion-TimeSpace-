from __future__ import annotations

import sys

from native_common import *


def analyze(label):
    folder = ROOT / 'runs' / label
    heavy = np.load(folder / 'heavy.npz')
    cold = np.load(folder / 'cold.npz')
    table = np.load(ROOT / 'runs/backgrounds/heavy.npz')
    names = heavy['names'].tolist()
    phase_of_n = interpolate.CubicSpline(table['heavy_efold'], table['phase_h'])
    field_of_n = interpolate.CubicSpline(table['heavy_efold'], table['phi_h'])
    velocity_of_n = interpolate.CubicSpline(table['heavy_efold'], table['phidot_h'])
    scales = heavy['values'][0, :, names.index('a')]
    phase = phase_of_n(np.log(scales))
    modes = heavy['modes']
    rows = []
    for center in [.0002, .000225, .00025]:
        middle = float(phase_of_n(math.log(center)))
        chosen = abs(phase-middle) <= 8*math.pi * (1+1e-8)
        offsets = (phase[chosen]-middle) / (8*math.pi)
        basis = np.column_stack([offsets**degree for degree in range(5)] +
            [offsets**degree * trig(2*phase[chosen]) for degree in range(3) for trig in [np.cos, np.sin]] +
            [np.cos(4*phase[chosen]), np.sin(4*phase[chosen])])

        def average(values):
            return float(np.linalg.lstsq(basis, np.asarray(values)[chosen], rcond=None)[0][0])

        background_rho = (velocity_of_n(np.log(scales))**2 + (scales * float(table['heavy_mass_mpc']) * field_of_n(np.log(scales)))**2) / 2
        abundance = average(scales * background_rho)
        for index, mode in enumerate(modes):
            data = heavy['values'][index]
            control = cold['values'][index]
            hubble = data[:, names.index('H')]
            heavy_delta = average(scales * data[:, names.index('mts_drho_h')]) / abundance
            heavy_pressure = average(scales * data[:, names.index('mts_dp_h')]) / abundance
            heavy_velocity = average(scales * mode * data[:, names.index('mts_q_h')] / hubble) / abundance
            center_hubble = average(hubble)
            kappa2 = (mode/(center*float(table['heavy_mass_mpc'])))**2
            sound2 = kappa2 / (math.sqrt(1+kappa2)+1)**2
            pressure_model = sound2 * (heavy_delta+3*heavy_velocity*(center_hubble/mode)**2)
            norm = max(abs(heavy_delta), abs(heavy_velocity) / max(1., mode/center_hubble*math.sqrt(sound2)), 1e-6)
            cold_native = average(data[:, names.index('delta_cdm')])
            cold_control = average(control[:, names.index('delta_cdm')])
            rows.append(dict(center_a=center, k_Mpc_inverse=float(mode), heavy_delta=heavy_delta,
                heavy_velocity_theta_over_H=heavy_velocity, heavy_pressure=heavy_pressure,
                averaged_pressure_prediction=pressure_model,
                pressure_mismatch_over_mode_norm=abs(heavy_pressure-pressure_model)/norm,
                heavy_mass_over_H=center*float(table['heavy_mass_mpc'])/center_hubble,
                background_comoving_density_native=abundance, cold_amplitude=cold_native,
                cold_control_amplitude=cold_control, cold_amplitude_ratio=cold_native/cold_control,
                phase_fit_points=int(chosen.sum()), phase_fit_condition_number=float(np.linalg.cond(basis))))
    return rows


def main():
    modest()
    labels = sys.argv[1:]
    folder = ROOT / 'results/early-analysis'
    folder.mkdir(parents=True, exist_ok=False)
    rows = {label: analyze(label) for label in labels}
    reference = rows[labels[-1]]
    comparisons = []
    for label in labels[:-1]:
        for earlier, later in zip(rows[label], reference):
            comparisons.append(dict(label=label, center_a=later['center_a'], k_Mpc_inverse=later['k_Mpc_inverse'],
                cold_ratio_relative_change=abs(earlier['cold_amplitude_ratio']/later['cold_amplitude_ratio']-1),
                heavy_delta_relative_change=abs(earlier['heavy_delta']-later['heavy_delta'])/max(abs(later['heavy_delta']), 1.),
                heavy_velocity_relative_change=abs(earlier['heavy_velocity_theta_over_H']-later['heavy_velocity_theta_over_H'])/max(abs(later['heavy_velocity_theta_over_H']), 1.)))
    finish(folder, dict(matches=rows, convergence_comparisons=comparisons,
        explicit_full_state_native_handoff_done=False, observational_fit=False), __file__,
        [ROOT / 'runs' / label / name for label in labels for name in ['cold.npz', 'heavy.npz', 'status.json']] +
        [ROOT / 'runs/backgrounds/heavy.npz'])
    print(json.dumps(dict(final_rows=[row for row in reference if row['center_a']==.00025],
        maximum_cold_ratio_change=max(row['cold_ratio_relative_change'] for row in comparisons),
        maximum_heavy_delta_change=max(row['heavy_delta_relative_change'] for row in comparisons)), indent=2), flush=True)


if __name__ == '__main__':
    main()
