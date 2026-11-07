from sourced_emission import *
from scipy import special


def main():
    modest()
    folder = ROOT / 'results/sourced-emission'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], [ROOT / 'sourced_emission.py', ROOT / 'emission_rates.py']
    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))
    for name, charge in [('gauntff.dat', None), ('gauntff_merged_Z01.dat', 1), ('gauntff_merged_Z02.dat', 2)]:
        table = GauntTable(ROOT / 'sources' / name, charge)
        gamma = 10 ** (table.gamma_start + table.step * np.arange(table.columns))
        frequency = 10 ** (table.u_start + table.step * np.arange(table.rows))
        recovered = table(gamma[None, :], frequency[:, None])
        error = float(np.max(abs(recovered / table.values - 1)))
        check(name + ': original grid, orientation, normalization reproduced', error < 1e-12, error)
        rejected = False
        try:
            table(1e-20, 1.)
        except ValueError:
            rejected = True
        check(name + ': out-of-range inputs rejected rather than extrapolated', rejected)
        inputs.append(table.path)
    basis = ConsistentBasis(24, 420, pivot=.1)
    rows = []
    for model in ['heavy', 'cold']:
        background = thermal_wave.thermal.ThermalBackground(model)
        merged = SourcedEmission(basis, background, 900, 81)
        nr = SourcedEmission(basis, background, 900, 81, True)
        values = []
        minimum_eigenvalue = math.inf
        for theta in np.geomspace(merged.temperatures[0], merged.temperatures[-1], 57):
            direct = merged.br_matrix(theta)
            interpolated = merged.at(theta, 'dcbr') - merged.at(theta, 'dc')
            values.append(float(linalg.norm(direct - interpolated) / linalg.norm(direct)))
            minimum_eigenvalue = min(minimum_eigenvalue, float(min(linalg.eigvalsh(interpolated))))
            assert np.isfinite(merged.br_rates(theta)).all()
        check(model + ': temperature interpolation agrees with direct sourced integral', max(values) < .002, max(values))
        check(model + ': BR damping remains positive after interpolation', minimum_eigenvalue > -1e-17, minimum_eigenvalue)
        equilibrium = basis.temperature * .17
        error = float(linalg.norm(merged.at(merged.temperatures[-1], 'dcbr') @ (equilibrium - basis.temperature * .17)))
        check(model + ': common photon-electron temperature is emission equilibrium', error == 0., error)
        check(model + ': inherited fully ionized electron density positive', background.electron0 > 0, background.electron0)
        check(model + ': Planck heat source predicts leading energy extraction', background.chi > 0, -background.chi * background.end)
        for theta in [merged.temperatures[0], merged.temperatures[-1]]:
            difference = float(np.max(abs(merged.br_rates(theta) / nr.br_rates(theta) - 1)))
            for frequency in [.001, .01, .1, 1., 8.]:
                index = np.argmin(abs(merged.frequency - frequency))
                absorption = merged.br_rates(theta)[index]
                dc = DC_CONSTANT * theta ** 2 / (1 + 14.16 * theta) * dc_absorption_shape(merged.frequency[index], 'dc')
                rows.append(dict(model=model, theta=float(theta), x=float(merged.frequency[index]),
                                 br_absorption_per_thomson_time=float(absorption),
                                 dc_absorption_per_thomson_time=float(dc), br_over_dc=float(absorption / dc),
                                 maximum_merged_NR_relative_rate_difference=difference))
        inputs.extend([background.parent.source, background.native_constants])
    write_json(folder / 'rates.json', rows)
    check('Dimensionless source has explicit number-to-Planck-fraction conversion', math.pi ** 4 / (30 * special.zeta(3)) > 0)
    sources = [dict(url='https://data.nublado.org/gauntff/' + name, path=str(ROOT / 'sources' / name),
                    sha256=digest(ROOT / 'sources' / name)) for name in ['gauntff.dat', 'gauntff_merged_Z01.dat', 'gauntff_merged_Z02.dat', 'license.txt']]
    for name, url in [('1109.6552.html', 'https://arxiv.org/html/1109.6552'), ('gauntff-index.html', 'https://data.nublado.org/gauntff/')]:
        sources.append(dict(url=url, path=str(ROOT / 'sources' / name), sha256=digest(ROOT / 'sources' / name)))
        inputs.append(ROOT / 'sources' / name)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        sources=sources, original_source_data_unmodified=True, confidence='Deterministic rate-table inputs, not observational confidence intervals.',
        physical_scope='Sourced leading DC and H/He free-free absorption/emission; merged NR/BHE tables, not full EH or DC redistribution.',
        inherited_constants_not_new_MTS_derivation=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
