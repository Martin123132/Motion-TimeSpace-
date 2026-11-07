from __future__ import annotations

import sys
import time
import traceback

from native_common import *


def main():
    modest()
    started = time.monotonic()
    folder = ROOT / 'runs' / sys.argv[1]
    folder.mkdir(parents=True, exist_ok=False)
    table_path = ROOT / 'runs/backgrounds/cold.npz'
    try:
        omega_m, slow_mass = previous.inherited_parameters()
        models = [('rebuilt-lcdm', previous.base_params(omega_m), 'lcdm-transfer.npz'),
            ('native-slow', params_for(table_path), 'cold-slow-transfer-0.0001.npz')]
        rows = []
        for name, params, baseline_name in models:
            print('Native cold control', name, flush=True)
            params.set_accuracy(AccuracyBoost=1.5)
            params.set_matter_power(redshifts=[10., 1., 0.], kmax=5., nonlinear=False, silent=True)
            params.Transfer.accurate_massive_neutrinos = True
            result = camb.get_results(params)
            transfer = result.get_matter_transfer_data().transfer_data
            sigma = result.get_sigma8()
            growth = result.get_fsigma8()
            np.savez_compressed(folder / (name + '.npz'), transfer=transfer, sigma8=sigma, fsigma8=growth)
            baseline_path = PARENT / 'runs/thermal-v3' / baseline_name
            baseline = np.load(baseline_path)
            comparisons = []
            valid = (transfer[0, :, 0] >= baseline['transfer'][0, 0, 0]) & (transfer[0, :, 0] <= baseline['transfer'][0, -1, 0])
            for column in [1, 2, 5, 6, 7, 8, 9, 10, 11, 12]:
                expected = interpolate.CubicSpline(np.log(baseline['transfer'][0, :, 0]), baseline['transfer'][column], axis=0)(np.log(transfer[0, valid, 0]))
                current = transfer[column, valid]
                comparisons.append(dict(column=column, normalized_max_error=float(np.max(abs(current-expected)) / max(np.max(abs(expected)), 1e-30))))
            row = dict(model=name, sigma8=sigma.tolist(), fsigma8=growth.tolist(),
                sigma8_max_relative_error=float(np.max(abs(sigma/baseline['sigma8']-1))),
                fsigma8_max_relative_error=float(np.max(abs(growth/baseline['fsigma8']-1))),
                transfer_comparisons=comparisons, transfer_finite=bool(np.isfinite(transfer).all()),
                rdrag_Mpc=result.get_derived_params()['rdrag'], baseline=str(baseline_path))
            rows.append(row)
            print(row, flush=True)
        finish(folder, dict(models=rows, elapsed_seconds=time.monotonic()-started,
            scalar_fields_evolved_directly=True, fluid_floor_used=False), __file__,
            [table_path] + list(folder.glob('*.npz')) + [PARENT / 'runs/thermal-v3' / name for _, _, name in models])
    except BaseException as error:
        write_json(folder / 'status.json', dict(state='failed', error=repr(error), traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
