from __future__ import annotations

from datetime import datetime, timezone
import argparse
import math

import numpy as np

from carrier import ROOT, BRANCH, PRIOR, PARENT, digest, read_json, write_json, modest_process, orbit_series, complex_value, damping, imported_hashes
from secular import geometry


def carrier_law(rows, step=.0005):
    lookup = {row['fractional_frequency_shift']: row for row in rows}
    center = lookup[0.]
    frequency = center['frequency']
    alpha = orbit_series(center['semilatus'])['angular_frequency_fraction']

    def derivative(key):
        return (complex_value(lookup[-2*step], key)-8*complex_value(lookup[-step], key)
                +8*complex_value(lookup[step], key)-complex_value(lookup[2*step], key))/(12*step)

    base = {key: complex_value(center, key) for key in ['reference_amplitude', 'delta_amplitude', 'horizon_amplitude']}
    second = {key: complex_value(center, key, 1)+alpha*derivative(key) for key in base}
    factor = 3*frequency**2/(4*np.pi)
    reference, difference, horizon = [base[key] for key in base]
    reference_second, difference_second, horizon_second = [second[key] for key in second]
    reference_power = factor*abs(reference)**2
    horizon_power = factor*abs(horizon)**2
    difference_power = factor*(2*(reference.conjugate()*difference).real+abs(difference)**2)
    reference_power_second = 2*factor*((reference.conjugate()*reference_second).real+alpha*abs(reference)**2)
    horizon_power_second = 2*factor*((horizon.conjugate()*horizon_second).real+alpha*abs(horizon)**2)
    difference_power_second = 2*factor*((reference_second.conjugate()*difference+reference.conjugate()*difference_second
                                          +difference.conjugate()*difference_second).real
                                        +alpha*(2*(reference.conjugate()*difference).real+abs(difference)**2))
    base_power = dict(BH=reference_power+horizon_power, body=reference_power+difference_power, difference=difference_power-horizon_power)
    second_power = dict(BH=reference_power_second+horizon_power_second, body=reference_power_second+difference_power_second,
                        difference=difference_power_second-horizon_power_second)
    action_second_geometry = -3/(8*np.pi)*(complex_value(center, 'difference_coefficient', 1)*complex_value(center, 'outgoing_source')
                             +complex_value(center, 'difference_coefficient')*complex_value(center, 'outgoing_source', 1))
    action_second = action_second_geometry+alpha*derivative('action')
    optical_second = 2*frequency*(action_second.imag+alpha*complex_value(center, 'action').imag)
    return dict(sector=center['sector'], azimuth=center['azimuth'], separation=center['separation'],
                semilatus=center['semilatus'], mass=center['mass'], frequency=frequency, alpha_phi=alpha,
                base_power=base_power, second_power=second_power,
                amplitudes0={key:[value.real,value.imag] for key,value in base.items()},
                amplitudes2={key:[value.real,value.imag] for key,value in second.items()},
                optical_second_relative_error=abs(optical_second-second_power['difference'])/max(abs(second_power['difference']), 1e-300))


def second_shrink(analytic, carriers, component, channel):
    selected = [row for row in analytic if component == 'combined_ell2' or row['sector'] == component]
    active = [row for row in carriers if component == 'combined_ell2' or row['sector'] == component]
    leading = damping(selected, component, channel)
    angular_second_flux = math.fsum(row['azimuth']/row['frequency']*(row['second_power'][channel]-row['alpha_phi']*row['base_power'][channel]) for row in active)
    energy_second_flux = math.fsum(row['second_power'][channel] for row in active)
    for row in selected:
        if row['harmonic'] == 0:
            continue
        power = (row['BH_infinity_energy']+row['BH_horizon_energy'] if channel == 'BH' else
                 row['body_infinity_energy'] if channel == 'body' else row['difference_total_energy'])
        angular_second_flux += row['azimuth']*power/row['frequency']
        energy_second_flux += power
    mass, semilatus = selected[0]['mass'], selected[0]['semilatus']
    state = geometry(mass, semilatus, 0.)
    angular_second = state['angular']/(2*(semilatus-3))
    angular_cross = -mass*(semilatus+6)/(4*(semilatus-3)**2.5)
    energy_factor = 1/(2*(semilatus-3))-2/(semilatus-2)**2
    energy_second = state['energy']*energy_factor
    energy_cross = state['energy_p']*energy_factor+state['energy']*(-1/(2*(semilatus-3)**2)+4/(semilatus-2)**3)
    base_shrink, gamma = leading['circular_p_rate_per_mu'], leading['Gamma_z_per_mu']
    second = (-angular_second_flux-angular_cross*base_shrink-angular_second*gamma)/state['angular_p']
    independent = (-energy_second_flux-energy_cross*base_shrink-energy_second*gamma)/state['energy_p']
    return dict(component=component, channel=channel, separation=selected[0]['separation_over_radius'], semilatus=semilatus,
                P0=base_shrink, Gamma0=gamma, P2=second, P2_energy_inverse=independent,
                energy_angular_P2_relative_error=abs(second-independent)/max(abs(second), 1e-300),
                energy_flux2=energy_second_flux, angular_flux2=angular_second_flux,
                P2_over_P0=second/base_shrink)


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', choices=['fine', 'coarse'], default='fine')
    parser.add_argument('--plan', choices=['pilot', 'nodes', 'full'], default='pilot')
    args = parser.parse_args()
    inputs = {}

    def load(path):
        value = read_json(path)
        assert value['state'] == 'complete'
        inputs[str(path)] = digest(path)
        return value

    labels = ['pilot-'+args.settings]+(['nodes-'+args.settings] if args.plan != 'pilot' else [])
    if args.plan == 'full':
        labels += ['extension-'+args.settings]
    modes = [row for label in labels for row in load(ROOT/'results'/label/'status.json')['rows']]
    old = load(PRIOR/'results'/('analytic-'+args.settings)/'status.json')['rows']
    prior_nodes = load(PARENT/'results'/('nodes-'+args.settings)/'status.json')
    old += prior_nodes['rows']
    separations = sorted({row['separation'] for row in modes})
    laws, alternate_laws, shrinkages = [], [], []
    for separation in separations:
        selected = [row for row in modes if abs(row['separation']-separation) < 1e-10]
        analytic = [row for row in old if abs(row['separation_over_radius']-separation) < 1e-10]
        assert len(analytic) == 7
        carriers, alternate = [], []
        for sector in ['polar', 'odd']:
            selected_sector = [row for row in selected if row['sector'] == sector]
            carriers.append(carrier_law(selected_sector))
            alternate.append(carrier_law(selected_sector, .001))
        laws.extend(carriers)
        alternate_laws.extend(alternate)
        for component in ['polar', 'odd', 'combined_ell2']:
            for channel in ['BH', 'body', 'difference']:
                result = second_shrink(analytic, carriers, component, channel)
                other = second_shrink(analytic, alternate, component, channel)
                result['frequency_step_relative_change'] = abs(result['P2']/other['P2']-1)
                shrinkages.append(result)
    finite_analysis = load(PRIOR/'results/analysis/status.json')
    finite_modes = load(PRIOR/'results'/('finite-'+args.settings)/'status.json')['rows']
    inherited_odd = load(BRANCH/'secular-actions-20261005/results'/('small-e-'+args.settings)/'status.json')['rows']
    finite_modes += [{**row, 'sector':'odd', 'azimuth':1} for row in inherited_odd]
    comparisons, amplitude_controls = [], []
    for result in [row for row in shrinkages if abs(row['separation']-5) < 1e-10]:
        finite = sorted([row for row in finite_analysis['finite_rates'] if row['settings'] == args.settings and
                         row['component'] == result['component'] and row['channel'] == result['channel']], key=lambda row:row['eccentricity'])
        estimates = [(row['semilatus_rate_per_mu']-result['P0'])/row['eccentricity']**2 for row in finite]
        extrapolated = (4*estimates[0]-estimates[1])/3
        comparisons.append(dict(component=result['component'], channel=result['channel'], predicted=result['P2'],
                                extrapolated=extrapolated, small_pair_relative_error=abs(extrapolated/result['P2']-1),
                                raw_estimates=estimates))
    for law in [row for row in laws if abs(row['separation']-5) < 1e-10]:
        finite = sorted([row for row in finite_modes if row['sector'] == law['sector'] and row['harmonic'] == 0], key=lambda row:row['eccentricity'])
        for key, predicted in law['amplitudes2'].items():
            estimates = []
            for row in finite:
                value = complex(row[key+'_real'], row[key+'_imag'])
                estimates.append((value-complex(*law['amplitudes0'][key]))/row['eccentricity']**2)
            extrapolated = (4*estimates[0]-estimates[1])/3
            amplitude_controls.append(dict(sector=law['sector'], amplitude=key, predicted=predicted,
                estimates=[[value.real,value.imag] for value in estimates], extrapolated=[extrapolated.real,extrapolated.imag],
                small_pair_relative_error=abs(extrapolated/complex(*predicted)-1)))
    directory = ROOT/'results'/('analysis-'+args.plan+'-'+args.settings)
    directory.mkdir(parents=True, exist_ok=False)
    result = dict(state='complete', script_sha256=digest(__file__), time_utc=datetime.now(timezone.utc).isoformat(),
                  input_hashes={**inputs, **imported_hashes()}, arguments=vars(args), carrier_laws=laws,
                  alternate_carrier_laws=alternate_laws, shrinkage_laws=shrinkages,
                  finite_e_comparisons=comparisons, finite_amplitude_controls=amplitude_controls)
    write_json(directory/'status.json', result, exclusive=True)
    print(dict(separations=separations, finite_comparisons=comparisons,
               amplitude_errors=[(row['sector'],row['amplitude'],row['small_pair_relative_error']) for row in amplitude_controls],
               optical_error=max(row['optical_second_relative_error'] for row in laws),
               energy_angular_error=max(row['energy_angular_P2_relative_error'] for row in shrinkages),
               step_control=max(row['frequency_step_relative_change'] for row in shrinkages)), flush=True)


if __name__ == '__main__':
    main()

