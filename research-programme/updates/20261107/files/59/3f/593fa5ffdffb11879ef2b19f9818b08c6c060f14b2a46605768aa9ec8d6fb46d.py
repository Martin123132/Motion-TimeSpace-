from rectangular_common import *
from nonlocal_dc import NonlocalEmission
import infrared_ladder


def response(basis, stiffness, rate, heat, source, gas_source, duration):
    alpha = 1 / duration
    forcing = rate * source
    matrix = alpha * basis.mass - rate * stiffness
    solved = linalg.solve(matrix, np.column_stack([forcing, -rate * stiffness @ basis.temperature]), assume_a='pos')
    free, susceptibility = solved[:, :-1], solved[:, -1]
    paired = rate * (basis.temperature @ source + gas_source)
    gas = (paired - alpha * (basis.energy @ free)) / (heat * (alpha + 1) + alpha * (basis.energy @ susceptibility))
    photon = free + susceptibility[:, None] * gas[None, :]
    work = duration * heat * gas
    photon_residual = alpha * basis.mass @ photon - rate * stiffness @ (photon - basis.temperature[:, None] * gas) - forcing
    gas_residual = heat * (alpha + 1) * gas + rate * basis.temperature @ stiffness @ (photon - basis.temperature[:, None] * gas) - rate * gas_source
    balance = basis.energy @ photon + heat * gas + work - duration * paired
    return photon, gas, dict(photon_equation_relative=float(np.linalg.norm(photon_residual) / max(np.linalg.norm(forcing), 1e-300)),
                            gas_equation_absolute=float(np.max(abs(gas_residual))),
                            energy_work_balance_absolute=float(np.max(abs(balance))))


def main():
    modest()
    folder = ROOT / 'results/frozen-coupled-response'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    ladder = infrared_ladder.InfraredLadder(prior.inherited.BACKGROUND / 'banks/infrared96-q700')
    overlap_path = ROOT / 'overlaps/midpoint-gould48/overlap.npz'
    overlap = dict(np.load(overlap_path))['joined_new_domain']
    locations = [ROOT / 'runs/midpoint-log32', ROOT / 'runs/midpoint-log48',
                 ROOT / 'controls/main-leading-control', ROOT / 'controls/refined-leading-control']
    arrays = [dict(np.load(path / 'source.npz')) for path in locations]
    checks, rows, dependencies, saved_arrays = [], [], [], {}
    for model_index, model in enumerate(['heavy', 'cold']):
        background = thermal_wave.thermal.ThermalBackground(model)
        local = background.at(spectra.coordinate)
        theta, heat = local['thermal_parameter'], background.chi
        rate = local['coefficient'] / theta
        emission = NonlocalEmission(ladder.basis, background, 'nonlocal-leading', inherited.SOURCE / 'banks/s960-i256')
        stiffness = ladder.at(theta, 0)[:96, :96] - emission.at(theta, 'dcbr')
        for duration in [1e-3, 1e-2]:
            photon_rows, gas_rows = [], []
            for location, values in zip(locations, arrays):
                difference = values['total'] - overlap
                selection = slice(2 * model_index, 2 * model_index + 2)
                photon, gas, metrics = response(ladder.basis, stiffness, rate, heat,
                    difference[1:-1, selection], difference[-1, selection], duration)
                photon_rows.append(photon)
                gas_rows.append(gas)
                key = model + '-' + location.name + '-' + str(duration)
                saved_arrays[key] = photon
                checks.append(dict(name='Frozen coupled equations and energy/work balance: ' + key,
                    passed=metrics['photon_equation_relative'] < 1e-7 and metrics['gas_equation_absolute'] < 1e-8 and metrics['energy_work_balance_absolute'] < 1e-14,
                    **metrics))
            comparisons = {}
            for first, second, label in [(0, 1, 'raw'), (2, 3, 'leading_control')]:
                difference = photon_rows[first] - photon_rows[second]
                numerator = np.sqrt(np.sum(difference * (ladder.basis.mass @ difference), axis=0))
                denominator = np.sqrt(np.sum(photon_rows[second] * (ladder.basis.mass @ photon_rows[second]), axis=0))
                comparisons[label] = dict(relative_spectral_response_change=(numerator / np.maximum(denominator, 1e-300)).tolist(),
                    gas_response_change=(gas_rows[first] - gas_rows[second]).tolist())
            rows.append(dict(model=model, duration=duration, gas_scaled=[value.tolist() for value in gas_rows],
                             response_comparisons=comparisons))
        dependencies += [*emission.inputs, background.parent.source, background.native_constants]
    np.savez(folder / 'response.npz', **saved_arrays)
    finish(folder, dict(checks=checks, rows=rows, constant_epoch_fraction=.5,
        full_parent_feedback_applied=False, new_parent_history=False, source_precision_gate_waived=False,
        scope='Conditional frozen-coefficient response of the retained full96-mode photon/gas system; diagnostic only while forcing resolution is unsettled.'),
        __file__, [*spectra.inputs, *ladder.inputs, *dependencies, overlap_path,
                   *[path / filename for path in locations for filename in ['status.json', 'source.npz']]])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
