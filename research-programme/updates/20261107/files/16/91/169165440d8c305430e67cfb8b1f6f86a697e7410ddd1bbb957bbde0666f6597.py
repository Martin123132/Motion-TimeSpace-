from __future__ import annotations

from datetime import datetime, timezone
import json
import math
import time

from growth_common import ROOT, Background, MODELS, MASS_RATIOS, FRACTIONS, WAVENUMBERS, SCALE_MASS, modest_process, read_json, save, solve_response, summary, conditions


def main():
    modest_process()
    assert read_json(ROOT / 'results/preflight/status.json')['scan_authorized']
    started = time.monotonic()
    folder = ROOT / 'runs/scan'
    folder.mkdir(parents=True, exist_ok=False)
    rows, rejected, sensitivity, backgrounds = [], [], [], []

    def log(event, payload):
        line = json.dumps(dict(time_utc=datetime.now(timezone.utc).isoformat(), event=event, **payload), allow_nan=False)
        with (folder / 'log.txt').open('a', encoding='utf-8') as handle:
            handle.write(line + '\n')

    for model in MODELS:
        background = Background(model)
        backgrounds.append(background.diagnostics)
        controls = {share: solve_response(background, 1e8, share, 0., pressure=False) for share in FRACTIONS}
        for mass_ratio in MASS_RATIOS:
            for share in FRACTIONS:
                for wave in WAVENUMBERS:
                    if time.monotonic() - started > 1200:
                        raise TimeoutError('20-minute scan budget reached; completed rows retained in run log.')
                    regime = conditions(background, mass_ratio, wave, 99.)
                    if not regime['accepted']:
                        entry = dict(model=model, mass_over_H0=mass_ratio, heavy_fraction=share, k_Mpc_inverse=wave, **regime)
                        rejected.append(entry)
                        log('outside_approximation', entry)
                        continue
                    solution = solve_response(background, mass_ratio, share, wave)
                    entry = summary(background, mass_ratio, share, wave, solution, controls[share])
                    rows.append(entry)
                    log('completed_response', entry)
            print(dict(event='mass_complete', model=model, mass=mass_ratio, completed=len(rows), seconds=time.monotonic() - started), flush=True)
        if model == 'ParentScalar_Lambda_zero':
            for start_z in [19., 49., 99.]:
                for preparation in ['equal', 'heavy_unperturbed']:
                    control = solve_response(background, SCALE_MASS, .5, 0., start_z, preparation, pressure=False)
                    for wave in [.1, 1., 5.]:
                        solution = solve_response(background, SCALE_MASS, .5, wave, start_z, preparation)
                        entry = summary(background, SCALE_MASS, .5, wave, solution, control, start_z, preparation)
                        sensitivity.append(entry)
                        log('initial_state_sensitivity', entry)
    save('scan', __file__, dict(backgrounds=backgrounds, rows=rows, excluded_outside_domain=rejected,
        initial_state_sensitivity=sensitivity, accepted_cases=len(rows), excluded_cases=len(rejected),
        total_requested_cases=len(MODELS) * len(MASS_RATIOS) * len(FRACTIONS) * len(WAVENUMBERS),
        elapsed_seconds=time.monotonic() - started, additional_growth_data_fitted=False,
        primordial_transfer_function_computed=False, background_parameters_refitted=False,
        galaxy_repo_modified=False, observed_mass_constraint_claim=False), [ROOT / 'results/preflight/status.json'])
    (folder / 'COMPLETE').write_text(datetime.now(timezone.utc).isoformat() + '\n', encoding='utf-8')
    print(dict(state='complete', accepted=len(rows), outside_domain=len(rejected), seconds=time.monotonic() - started), flush=True)


if __name__ == '__main__':
    main()
