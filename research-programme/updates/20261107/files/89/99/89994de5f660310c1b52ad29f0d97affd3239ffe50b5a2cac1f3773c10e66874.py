from emission_response import *
from increment_emitting_geometry import IncrementEmittingGeometry


def main():
    modest()
    folder = ROOT / 'results/frame-and-gas-pairing'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], [ROOT / 'emission_response.py', PARENT / 'increment_emitting_geometry.py']
    frequency, measure = thermal_wave.frequency_quadrature(1000)
    for model in ['heavy', 'cold']:
        geometry = IncrementEmittingGeometry(model, model + '-ir96-integrated-6400')
        response = EmissionResponse(geometry)
        inputs.extend(response.inputs)
        basis = geometry.basis
        values, derivative = basis.evaluate(frequency), basis.derivative(frequency)
        for expansion in [.1, math.log(10)]:
            data = [response.at(expansion, coordinate) for coordinate in frequency]
            source = np.array([row['source'] for row in data])
            density_source = np.array([row['density_source'] for row in data])
            br_source = np.array([row['br_source'] for row in data])
            boost = np.array([row['boost'] for row in data])
            heat = float((measure * frequency) @ source)
            density_heat = float((measure * frequency) @ density_source)
            br_heat = float((measure * frequency) @ br_source)
            boost_weak = (2 * values + frequency[:, None] * derivative).T @ (measure * source)
            paired_momentum = float(basis.temperature @ boost_weak / 3)
            strong_momentum = float((measure * frequency) @ boost / 3)
            edges = np.array([basis.minimum, basis.maximum])
            edge_sources = np.array([response.at(expansion, coordinate)['source'] for coordinate in edges])
            edge_planck = 1 / np.expm1(edges)
            edge_flux = edges ** 4 * edge_planck * (1 + edge_planck) * edge_sources / I3
            boundary = float((edge_flux[-1] - edge_flux[0]) / 3)
            scale = max(abs(heat), 1e-30)
            checks.append(check(model + ' boosted photon four-force energy/momentum identity s=' + str(expansion), abs(paired_momentum - heat) / scale, 1e-10))
            checks.append(check(model + ' strong boost plus finite-window edge s=' + str(expansion), abs(strong_momentum + boundary - heat) / scale, .002))
            specific_gas = -(density_heat - heat)
            checks.append(check(model + ' specific gas heat retains ion source after opacity cancellation s=' + str(expansion), abs(specific_gas + br_heat) / scale, 1e-12))
            paired_energy = np.array([density_heat, -density_heat])
            paired_current = np.array([paired_momentum, -paired_momentum])
            checks.append(check(model + ' opposite photon/gas four-force signs s=' + str(expansion), max(abs(np.sum(paired_energy)), abs(np.sum(paired_current))) / scale, 1e-14))
            rows.append(dict(model=model, expansion=expansion, background_energy_source=heat,
                density_energy_source=density_heat, specific_gas_density_source=specific_gas,
                bremsstrahlung_energy_source=br_heat, boost_momentum=paired_momentum,
                raw_finite_window_boost=strong_momentum, moving_window_correction=boundary))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        scope='Covariant transformation and paired moments of the retained isotropic emission source; not the missing general anisotropic DC redistribution.',
        moving_frequency_window_boundary_accounted=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
