from __future__ import annotations

import argparse
import csv
import json
import traceback

from radiation_common import *


def emit_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='thermal')
    arguments = parser.parse_args()
    modest_process()
    started = time.monotonic()
    run_folder = ROOT / 'runs' / arguments.label
    run_folder.mkdir(parents=True, exist_ok=False)
    log_path = run_folder / 'log.txt'
    status_path = run_folder / 'status.json'

    def progress(event, **data):
        row = dict(event=event, elapsed_seconds=time.monotonic() - started, **data)
        with log_path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(row) + '\n')
        status_path.write_text(json.dumps(dict(state='running', **row)), encoding='utf-8')
        print(row, flush=True)

    try:
        omega_m, slow_mass = inherited_parameters()
        checkpoints = []
        native_rows = []
        saved_files = []
        exact = None
        calibration = []
        displacement = None
        for fraction in [0., .5]:
            progress('start_branch', fraction=fraction)
            species = StandardSpecies(omega_m, fraction)
            target = fraction * omega_m
            dust = lambda efold: (target * np.exp(-3 * np.asarray(efold)), -3 * target * np.exp(-3 * np.asarray(efold)))
            slow_initial, reference_slow, reference_flatness = solve_slow(species, dust, slow_mass)
            if fraction:
                displacement, exact, calibration = exact_heavy(species, target, slow_mass**2 * slow_initial**2)
                switches = [.00015, .0002, .00025]
            else:
                switches = [0.]
            for switch in switches:
                bridge = density_bridge(exact, target, switch) if fraction else dust
                slow_initial, slow_solution, flatness = solve_slow(species, bridge, slow_mass)
                table = full_table(species, slow_solution, slow_mass, bridge, exact if fraction else None)
                progress('native_background', fraction=fraction, switch=switch, table_nodes=len(table['scale']))
                params, native = native_background(species, table)
                query_n = np.linspace(START, 0., 2401)
                query_a = np.exp(query_n)
                model_expansion = np.exp(interpolate.CubicSpline(table['efold'], .5 * np.log(table['expansion2']))(query_n))
                native_expansion = native.hubble_parameter(1 / query_a - 1) / H0
                expansion_error = float(np.max(abs(native_expansion / model_expansion - 1)))
                derived = native.get_derived_params()
                independent_rd = sound_horizon_quadrature(species, table, derived['zdrag'])
                thermal = native.get_background_redshift_evolution(np.array([2000., 1500., 1100., 800., 100.]), vars=['x_e', 'T_b', 'opacity'])
                before_onset = table['scale'] <= EXACT_END
                frozen_error = float(np.max(abs(table['slow_density'][before_onset] / (slow_mass**2 * slow_initial**2) - 1)))
                row = dict(fraction=fraction, switch_a=switch, omega_m=omega_m,
                    H0=H0, slow_mass_over_H0=slow_mass, heavy_mass_over_H0=HEAVY_MASS,
                    slow_initial=slow_initial, flatness_error=abs(flatness - 1),
                    standard_species_coefficients=species.coefficients,
                    native_derived={key: float(value) for key, value in derived.items()},
                    sound_horizon_quadrature_Mpc=independent_rd,
                    sound_horizon_relative_difference=abs(independent_rd / derived['rdrag'] - 1),
                    maximum_native_H_relative_difference=expansion_error,
                    early_frozen_slow_density_relative_change=frozen_error,
                    background_table_nodes=len(table['scale']), minimum_effective_w=float(np.min(table['dark_w'])),
                    thermal_at_z=[2000., 1500., 1100., 800., 100.],
                    thermal_values={key: value.tolist() for key, value in thermal.items()},
                    bao=bao_score(native), heavy_perturbations_computed=False)
                checkpoints.append(row)
                if not fraction or switch == .0002:
                    stem = 'cold-slow' if not fraction else 'heavy-slow'
                    path = run_folder / (stem + '-background.npz')
                    np.savez_compressed(path, **table)
                    saved_files.append(path)
                    data_path = run_folder / (stem + '-bao-residuals.csv')
                    emit_csv(data_path, row['bao']['rows'])
                    saved_files.append(data_path)
                    if not fraction:
                        for floor in [1e-4, 3e-4, 0.]:
                            progress('cold_native_transfer', floor=floor)
                            transfer_params = species.params.copy()
                            transfer_params.set_dark_energy(use_tabulated_w=True, wde_a_array=table['scale'],
                                wde_w_array=np.maximum(table['dark_w'], -1 + floor), cs2=1., dark_energy_model='fluid' if floor else 'ppf')
                            transfer_params.set_matter_power(redshifts=[10., 1., 0.], kmax=5., nonlinear=False, silent=True)
                            transfer_params.Transfer.accurate_massive_neutrinos = True
                            transfer_params.set_accuracy(AccuracyBoost=1.5)
                            transfer = camb.get_results(transfer_params)
                            spectra = transfer.get_matter_transfer_data()
                            transfer_path = run_folder / ('cold-slow-transfer-' + str(floor) + '.npz')
                            np.savez_compressed(transfer_path, transfer=spectra.transfer_data, sigma8=transfer.get_sigma8(), fsigma8=transfer.get_fsigma8())
                            saved_files.append(transfer_path)
                            native_rows.append(dict(model='slow_parent_F0', floor=floor, implementation='fluid' if floor else 'ppf',
                                sigma8=transfer.get_sigma8().tolist(), fsigma8=transfer.get_fsigma8().tolist(),
                                transfer_shape=list(spectra.transfer_data.shape),
                                all_finite=bool(np.all(np.isfinite(spectra.transfer_data))),
                                saved_path=str(transfer_path), actual_two_field_prediction=False))
                progress('branch_saved', fraction=fraction, switch=switch, rdrag=derived['rdrag'], bao_chi2=row['bao']['chi2_fixed_physical_rd'], H_error=expansion_error)

        lcdm_params = base_params(omega_m)
        lcdm_params.set_matter_power(redshifts=[10., 1., 0.], kmax=5., nonlinear=False, silent=True)
        lcdm_params.Transfer.accurate_massive_neutrinos = True
        lcdm_params.set_accuracy(AccuracyBoost=1.5)
        progress('lcdm_native_transfer')
        lcdm = camb.get_results(lcdm_params)
        transfer_path = run_folder / 'lcdm-transfer.npz'
        np.savez_compressed(transfer_path, transfer=lcdm.get_matter_transfer_data().transfer_data,
            sigma8=lcdm.get_sigma8(), fsigma8=lcdm.get_fsigma8())
        saved_files.append(transfer_path)
        baseline = dict(model='LCDM_matched_budget', derived={key: float(value) for key, value in lcdm.get_derived_params().items()},
            bao=bao_score(lcdm), sigma8=lcdm.get_sigma8().tolist(), fsigma8=lcdm.get_fsigma8().tolist())
        save(arguments.label, __file__, dict(branches=checkpoints, native_cold_transfer_rows=native_rows,
            lcdm=baseline, heavy_initial=displacement, heavy_calibration=calibration,
            direct_two_field_Boltzmann_prediction=False, primordial_covariance_derived=False,
            new_observations_used=['DESI DR2 Gaussian BAO 13-row covariance at fixed inherited late parameters'],
            parameter_fit=False, galaxy_work_modified=False, elapsed_seconds=time.monotonic() - started), saved_files)
        progress('complete')
        status_path.write_text(json.dumps(dict(state='complete', elapsed_seconds=time.monotonic() - started)), encoding='utf-8')
        (run_folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    except Exception as error:
        status_path.write_text(json.dumps(dict(state='failed', error=repr(error), elapsed_seconds=time.monotonic() - started)), encoding='utf-8')
        with log_path.open('a', encoding='utf-8') as handle:
            handle.write(traceback.format_exc())
        raise


if __name__ == '__main__':
    run()

