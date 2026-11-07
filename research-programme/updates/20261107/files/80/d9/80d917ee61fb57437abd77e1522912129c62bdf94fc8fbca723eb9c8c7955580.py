from __future__ import annotations

import json
import math
import time
import traceback

import numpy as np
from scipy import optimize

import radiation_common as common


def main():
    common.modest_process()
    started = time.monotonic()
    folder = common.ROOT / 'runs/physical-bao-profile'
    folder.mkdir(parents=True, exist_ok=False)
    progress_path = folder / 'status.json'
    log_path = folder / 'log.txt'
    omega_m, reference_slow_mass = common.inherited_parameters()
    reference_heavy_mass = common.HEAVY_MASS
    evaluations = []
    fits = []
    cache = {}

    def evaluate(model, hubble):
        key = (model, float(hubble))
        if key in cache:
            return cache[key]
        common.H0 = float(hubble)
        common.HEAVY_MASS = reference_heavy_mass * 70 / hubble
        slow_mass = reference_slow_mass * 70 / hubble
        if model == 'LCDM':
            params = common.base_params(omega_m)
            native = common.camb.get_background(params)
            row = dict(flatness_error=0., heavy_abundance_relative_error=0., slow_initial=None)
        else:
            fraction = .5 if model == 'parent_heavy_half' else 0.
            species = common.StandardSpecies(omega_m, fraction)
            target = fraction * omega_m
            dust = lambda efold: (target * np.exp(-3 * np.asarray(efold)), -3 * target * np.exp(-3 * np.asarray(efold)))
            initial, solution, flatness = common.solve_slow(species, dust, slow_mass)
            if fraction:
                displacement, exact, history = common.exact_heavy(species, target, slow_mass**2 * initial**2)
                heavy = common.density_bridge(exact, target, .0002)
                initial, solution, flatness = common.solve_slow(species, heavy, slow_mass)
                abundance_error = abs(history[-1]['relative_error'])
            else:
                exact, heavy, abundance_error = None, dust, 0.
            table = common.full_table(species, solution, slow_mass, heavy, exact)
            _, native = common.native_background(species, table)
            row = dict(flatness_error=abs(flatness - 1), heavy_abundance_relative_error=abundance_error, slow_initial=initial)
        score = common.bao_score(native)
        row.update(model=model, H0=float(hubble), chi2=score['chi2_fixed_physical_rd'],
            physical_rd_Mpc=score['physical_rd_Mpc'], shape_chi2=score['chi2_profiled_rd_shape_only'],
            profiled_rd_Mpc=score['profiled_rd_Mpc'], mu_over_H0=slow_mass if model != 'LCDM' else None,
            M_over_H0=common.HEAVY_MASS if model == 'parent_heavy_half' else None,
            elapsed_seconds=time.monotonic() - started)
        evaluations.append(row)
        with log_path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(row) + '\n')
        progress_path.write_text(json.dumps(dict(state='running', latest=row, evaluations=len(evaluations))), encoding='utf-8')
        print(row, flush=True)
        cache[key] = row
        return row

    try:
        for model in ['LCDM', 'parent_cold', 'parent_heavy_half']:
            result = optimize.minimize_scalar(lambda hubble: evaluate(model, hubble)['chi2'],
                bounds=(55., 85.), method='bounded', options=dict(xatol=.003, maxiter=16))
            assert result.success, result.message
            best = dict(evaluate(model, float(result.x)))
            best.update(converged=bool(result.success), evaluations=int(result.nfev), bounds=[55., 85.],
                edge_hit=bool(min(result.x - 55, 85 - result.x) < .3))
            fits.append(best)
        common.save('physical-bao-profile', __file__, dict(fits=fits, evaluations=evaluations,
            common_fixed_omega_m=omega_m, common_fixed_ombh2=common.OMBH2,
            common_neutrino_mass_eV=common.NEUTRINO_MASS, common_H0_bounds=[55., 85.],
            physical_scalar_masses_held_fixed=True, reference_H0=70.,
            reference_slow_mass_over_H0=reference_slow_mass,
            reference_heavy_mass_over_H0=reference_heavy_mass,
            changed_cosmological_fit_parameters=['H0'], standard_flatness_and_abundance_shoots_not_data_fits=True,
            full_joint_SN_BAO_CMB_fit=False, independent_holdout=False, information_criteria_reported=False,
            full_two_field_Boltzmann_prediction=False, elapsed_seconds=time.monotonic() - started),
            [common.ROOT / 'results/thermal-v3/status.json'])
        progress_path.write_text(json.dumps(dict(state='complete', elapsed_seconds=time.monotonic() - started)), encoding='utf-8')
        (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    except Exception as error:
        progress_path.write_text(json.dumps(dict(state='failed', error=repr(error))), encoding='utf-8')
        with log_path.open('a', encoding='utf-8') as handle:
            handle.write(traceback.format_exc())
        raise


if __name__ == '__main__':
    main()

