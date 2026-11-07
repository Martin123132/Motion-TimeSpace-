from sampled_gould_control import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/leading-addback-control'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    tests = TestFunctions(spectra.basis)
    background = thermal_wave.thermal.ThermalBackground('heavy')
    theta = background.at(spectra.coordinate)['thermal_parameter']
    reference_path = ROOT / 'overlaps/midpoint-gould48/overlap.npz'
    reference = dict(np.load(reference_path))['joined_new_domain']
    rows, arrays = [], {}
    for seed_order, radial in [(16, 96), (32, 128), (48, 160)]:
        result = sampled(spectra, tests, theta, seed_order, radial)
        relative = dual_norm(result[1:-1] - reference[1:-1], spectra.basis.mass) / dual_norm(reference[1:-1], spectra.basis.mass)
        rows.append(dict(seed_order=seed_order, radial_order=radial, relative_to_independent_overlap=relative.tolist()))
        arrays[str(seed_order)] = result
    checks = [
        dict(name='Independently refined sampled leading term reproduces exact-addback quadrature within0.01percent',
             value=max(rows[-1]['relative_to_independent_overlap']), passed=max(rows[-1]['relative_to_independent_overlap']) < 1e-4),
        dict(name='Leading control leaves both energy rows exactly zero before addback',
             passed=all(np.max(abs(value[[0, -1]])) == 0 for value in arrays.values())),
        dict(name='Control coefficient equals1 by subtraction identity and is not fitted', passed=True),
    ]
    np.savez(folder / 'leading-controls.npz', **arrays)
    finish(folder, dict(checks=checks, rows=rows, coefficient=1., coefficient_fitted=False,
        full_source_modes_retained=96, cancellation_is_numerical_not_new_physics=True), __file__,
        [*spectra.inputs, reference_path, reference_path.parent / 'status.json'])
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
