import argparse
from compare_backgrounds import load
from integrated_dc import *


def main(arguments):
    modest()
    folder = ROOT / 'results/physical-summary'
    folder.mkdir(parents=True, exist_ok=False)
    frequency, measure = thermal_wave.frequency_quadrature(1200)
    samples, checks, inputs, records = [], [], [], []
    for model in ['heavy', 'cold']:
        controls = {}
        for label, suffix in [('none', 'none'), ('dc', 'dc'), ('dcbr', 'integrated')]:
            name = model + '-ir96-' + suffix + '-' + str(arguments.steps)
            basis, saved, packet, extra = load(name)
            potential = basis.evaluate(frequency) @ saved['profiles'][-1]
            heat = float(saved['heat'])
            gas = float(saved['temperature_scaled'][-1])
            number_temperature = (measure @ potential) / (measure @ frequency)
            shape = potential - frequency * number_temperature
            controls[label] = dict(potential=potential, shape=shape, gas=gas, heat=heat, packet=packet,
                                   number_fraction=float(heat * saved['number_scaled'][-1] * math.pi ** 4 / (30 * special.zeta(3))),
                                   energy_fraction=float(heat * saved['energy_scaled'][-1]))
            inputs.extend(extra)
        base_norm = math.sqrt(float(measure @ controls['none']['shape'] ** 2))
        for label in ['none', 'dc', 'dcbr']:
            control = controls[label]
            norm = math.sqrt(float(measure @ control['shape'] ** 2))
            record = dict(model=model, emission=label, final_energy_fraction=control['energy_fraction'],
                          final_number_fraction=control['number_fraction'],
                          final_temperature_fraction=control['heat'] * control['gas'],
                          temperature_removed_shape_ratio_to_no_emission=norm / base_norm)
            records.append(record)
            samples.append(np.column_stack([frequency, control['heat'] * control['potential'],
                                           control['heat'] * control['shape'],
                                           control['heat'] * (control['potential'] - frequency * control['gas'])]))
        expected_energy = -controls['dcbr']['heat'] * math.log(10)
        energy_error = abs(controls['dcbr']['energy_fraction'] / expected_energy - 1)
        checks.extend([
            dict(name=model + ': known leading baryon-cooling energy follows -chi ln(a_end/a_start)', passed=energy_error < .002, value=energy_error),
            dict(name=model + ': no-emission control conserves number', passed=abs(controls['none']['number_fraction']) < 1e-16, value=controls['none']['number_fraction']),
            dict(name=model + ': sourced net photon absorption in cooling background', passed=controls['dcbr']['number_fraction'] < 0, value=controls['dcbr']['number_fraction']),
            dict(name=model + ': additional BR absorption is resolved rather than omitted', passed=abs(controls['dcbr']['number_fraction']) > abs(controls['dc']['number_fraction']), value=controls['dcbr']['number_fraction'] / controls['dc']['number_fraction'])])
    np.savez_compressed(folder / 'spectra.npz', samples=samples)
    write_json(folder / 'physical-results.json', records)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        results=records, physical_scope='Homogeneous fully ionized a=1e-6 to1e-5 background, not a present-day sky prediction.',
        same_parents_no_new_fit=True, source_functional='Integrated Planck ambient Gould DC plus tabulated H/He BR.'), __file__,
        [ROOT / 'compare_backgrounds.py', ROOT / 'integrated_dc.py', ROOT / 'sourced_emission.py', *inputs])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], results=records)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=6400)
    main(parser.parse_args())
