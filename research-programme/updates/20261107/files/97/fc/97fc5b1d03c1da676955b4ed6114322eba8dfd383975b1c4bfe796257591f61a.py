from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy.integrate import simpson, cumulative_simpson

from transient import ROOT, energy_series, dependencies, digest, read_json, save, modest_process


def analyze(label, step, target):
    path = ROOT/'results'/label/'transfer.npz'
    archive = np.load(path)
    time = np.arange(-6000., 6000.+step/2, step)
    series = energy_series(time, archive)
    energy = series['bulk']+series['surface']
    residual = series['bulk_rate']+series['surface_rate']-series['work']+series['flux']
    cumulative_work = cumulative_simpson(series['work'], x=time, initial=0)
    cumulative_flux = cumulative_simpson(series['flux'], x=time, initial=0)
    cumulative_error = energy-energy[0]-cumulative_work+cumulative_flux
    frequencies, weights, amplitudes = (archive[key] for key in ['frequencies', 'frequency_weights', 'amplitudes'])
    source_index = int(archive['source_index'])
    work_spectral = np.pi*np.sum(weights*amplitudes**2*frequencies*archive['green'][:, 0, source_index].imag)
    infinity_spectral = np.pi*np.sum(weights*amplitudes**2*frequencies**2*abs(archive['infinity'])**2)
    detector_spectral = np.pi*np.sum(weights*amplitudes**2*frequencies*
        np.imag(np.conj(archive['green'][:, 0, -1])*archive['green'][:, 1, -1]))
    maximum_power = float(max(abs(series['work'])))
    positive_work = float(simpson(np.maximum(series['work'], 0), x=time))
    negative_work = float(simpson(np.minimum(series['work'], 0), x=time))
    metrics = dict(time_step=step, window=[float(time[0]), float(time[-1])],
        peak_total_energy=float(max(energy)), peak_bulk_energy=float(max(series['bulk'])),
        peak_boundary_energy=float(max(series['surface'])), peak_boundary_kinetic=float(max(series['surface_kinetic'])),
        endpoint_energy_fraction=float(max(energy[0], energy[-1])/max(energy)),
        endpoint_source_amplitude=float(max(abs(series['source'][0]), abs(series['source'][-1]))),
        work_spectral=float(work_spectral), infinity_spectral=float(infinity_spectral),
        detector_spectral=float(detector_spectral),
        source_work_window=float(simpson(series['work'], x=time)),
        detector_flux_window=float(simpson(series['flux'], x=time)),
        infinity_flux_window=float(simpson(series['radiation'], x=time)),
        positive_source_work=positive_work, negative_source_work=negative_work,
        emitted_over_peak_stored=float(infinity_spectral/max(energy)),
        differential_balance_relative=float(max(abs(residual))/maximum_power),
        cumulative_balance_over_peak_energy=float(max(abs(cumulative_error))/max(energy)),
        net_balance_over_emitted_energy=float(abs(energy[-1]-energy[0]-cumulative_work[-1]+cumulative_flux[-1])/infinity_spectral),
        spectral_balance_relative=float(abs(work_spectral-infinity_spectral)/infinity_spectral),
        detector_spectral_balance_relative=float(abs(detector_spectral-infinity_spectral)/infinity_spectral),
        work_window_error=float(abs(simpson(series['work'], x=time)/work_spectral-1)),
        detector_window_error=float(abs(simpson(series['flux'], x=time)/detector_spectral-1)),
        infinity_window_error=float(abs(simpson(series['radiation'], x=time)/infinity_spectral-1)),
        missing_surface_relative=float(max(abs(series['bulk_rate']-series['work']+series['flux']))/maximum_power),
        reversed_flux_relative=float(max(abs(series['bulk_rate']+series['surface_rate']-series['work']-series['flux']))/maximum_power),
        reversed_source_relative=float(max(abs(series['bulk_rate']+series['surface_rate']+series['work']+series['flux']))/maximum_power),
        surface_exchange_relative=float(max(abs(series['surface_rate']-series['boundary_velocity']*series['boundary_slope']))/maximum_power),
        minimum_instantaneous_detector_flux=float(min(series['flux'])),
        maximum_instantaneous_detector_flux=float(max(series['flux'])))
    name = label+'-time.npz'
    np.savez_compressed(target/name, **series, cumulative_work=cumulative_work,
        cumulative_flux=cumulative_flux, cumulative_balance_error=cumulative_error, differential_balance=residual)
    return metrics, path, target/name


def main():
    modest_process()
    target = ROOT/'results/packet'
    target.mkdir(parents=True, exist_ok=False)
    inputs = dependencies()
    outputs, metrics = {}, {}
    for label, step in [('checked-coarse', 2.), ('checked-fine', 1.)]:
        result, source, archive = analyze(label, step, target)
        metrics[label] = result
        inputs[str(source)] = digest(source)
        inputs[str(source.parent/'status.json')] = digest(source.parent/'status.json')
        outputs[archive.name] = digest(archive)
        print(dict(label=label, **result), flush=True)
    coarse = np.load(target/'checked-coarse-time.npz')
    fine = np.load(target/'checked-fine-time.npz')
    waveform_refinement = {}
    for key in ['source', 'bulk', 'surface', 'work', 'flux', 'radiation']:
        waveform_refinement[key] = float(max(abs(coarse[key]-fine[key][::2]))/max(abs(fine[key])))
    metric_refinement = {key:abs(metrics['checked-coarse'][key]/metrics['checked-fine'][key]-1)
        for key in ['peak_total_energy', 'peak_boundary_energy', 'work_spectral', 'infinity_spectral',
                    'source_work_window', 'detector_flux_window', 'infinity_flux_window']}
    path = target/'energy-ledger.csv'
    columns = ['time', 'source', 'bulk', 'surface', 'surface_kinetic', 'surface_potential',
               'work', 'flux', 'radiation', 'cumulative_work', 'cumulative_flux',
               'cumulative_balance_error', 'differential_balance']
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(zip(*(fine[key] for key in columns)))
    outputs[path.name] = digest(path)
    report = save(target, Path(__file__), dict(input_hashes=inputs, output_hashes=outputs,
        metrics=metrics, waveform_refinement=waveform_refinement, metric_refinement=metric_refinement,
        csv_rows=len(fine['time']), finite_duration='Finite observation window; band-limited packet has nonzero tails.',
        source_work_is_canonical_probe=True, physical_inspiral_source_claimed=False,
        energy_units='N/R times reported numbers', time_units='R times reported numbers',
        infinity_time='Asymptotic retarded time in units R; do not subtract its cumulative flux from finite-radius storage at equal coordinate time.'))
    print(dict(state=report['state'], waveform_refinement=waveform_refinement, metric_refinement=metric_refinement), flush=True)


if __name__ == '__main__':
    main()

