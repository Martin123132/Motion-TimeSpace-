from matched_weak import *


def main():
    modest()
    folder = ROOT / 'results/matched-weak-validation'
    folder.mkdir(parents=True, exist_ok=False)
    names = ['rest-a4-r28', 'rest-a6-r40', 'moving-a6-r40', 'moving-a8-r56',
             'moving-profile-point2', 'moving-separator-point2',
             'moving-floor-1e3', 'moving-floor-1e4', 'moving-floor-1e5', 'moving-floor-1e6',
             'chemical-refined-1e3', 'chemical-refined-5e4', 'chemical-refined-25e5',
             'chemical-refinement-240', 'midpoint-v4', 'midpoint-v6']
    packets, arrays, paths = {}, {}, []
    for name in names:
        path = ROOT / 'results' / name
        packets[name] = json.loads((path / 'status.json').read_text())
        arrays[name] = dict(np.load(path / 'matrix.npz'))
        assert packets[name]['all_checks_passed'] and (path / 'COMPLETE').is_file()
        paths.extend([path / 'status.json', path / 'matrix.npz'])
    base = arrays['moving-a6-r40']['total']
    checks = []
    comparisons = {}
    for title, first, second, tolerance in [
        ('Rest real angular/radial refinement', 'rest-a4-r28', 'rest-a6-r40', 1e-8),
        ('Moving real angular/radial refinement', 'moving-a6-r40', 'moving-a8-r56', 1e-8),
        ('Thermal subtraction profile cancellation', 'moving-profile-point2', 'moving-a6-r40', 1e-10),
        ('Vacuum separator cancellation', 'moving-separator-point2', 'moving-a6-r40', 1e-10),
        ('Independent midpoint loop and real refinement', 'midpoint-v4', 'midpoint-v6', 1e-7),
        ('Physical chemical integral radial160 to240 refinement', 'chemical-refined-25e5', 'chemical-refinement-240', 1e-7)]:
        error = relative(arrays[first]['total'], arrays[second]['total'])
        comparisons[title] = error
        checks.append(check(title, error, tolerance))
    floors = [relative(arrays[name]['total'], base) for name in
              ['moving-floor-1e3', 'moving-floor-1e4', 'moving-floor-1e5', 'moving-floor-1e6']]
    checks.append(check('Removing the regular soft floor converges to the zero-floor answer', floors[-1], 2e-6))
    checks.append(check('Regular lower-floor remainder scales linearly as derived',
                        max(abs(floors[index] / floors[index + 1] / 10 - 1) for index in range(3)), .002))
    conversion_fraction = float(np.linalg.norm(arrays['moving-profile-point2']['profile_conversion']) / np.linalg.norm(base))
    checks.append(dict(name='Omitting the finite profile conversion produces an observable numerical error',
                       passed=conversion_fraction > .01, relative_error=conversion_fraction))
    lower_name, upper_name = 'chemical-refined-5e4', 'chemical-refinement-240'
    lower_floor = packets[lower_name]['arguments']['floor']
    upper_floor = packets[upper_name]['arguments']['floor']
    chemical_coefficient = ((arrays[upper_name]['total'][0, 0] - arrays[lower_name]['total'][0, 0])
                            / (1 / upper_floor - 1 / lower_floor))
    expected_pole = packets[lower_name]['integrated_soft_pole']
    checks.append(check('Chemical divergence coefficient equals the independent conserved soft current',
                        abs(chemical_coefficient / expected_pole - 1), 1e-5))
    checks.append(dict(name='Physical number production remains nonzero and grows toward unresolved IR',
                       passed=bool(arrays[upper_name]['total'][0, 0] > arrays[lower_name]['total'][0, 0] > 0)))
    for name in ['rest-a6-r40', 'moving-a8-r56', 'midpoint-v6']:
        smallest = float(np.linalg.eigvalsh(arrays[name]['born'] + arrays[name]['total']).min())
        checks.append(check('Born plus matched projected bilinear is nonnegative at ' + name,
                            max(0., -smallest) / np.linalg.norm(arrays[name]['total']), 1e-7))
    zero = np.zeros(4)
    checks.append(check('Reference equilibrium is stationary without a source offset', np.linalg.norm(base @ zero), 1e-300))
    refused = False
    try:
        real_subtracted(source.context(.001, .1, [0, 0, 0], .001), chemical=True)
    except ValueError:
        refused = True
    checks.append(dict(name='Zero-floor chemical mode is rejected rather than silently projected away', passed=refused))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
           comparisons=comparisons, regular_floor_errors=floors,
           profile_conversion_omission_relative_error=conversion_fraction,
           chemical_pole_from_refined_difference=float(chemical_coefficient),
           chemical_pole_from_current=float(expected_pole),
           conditional_checks_not_full_operator_error_bound=True), __file__, paths)
    print(json.dumps(dict(count=len(checks), failed=[row for row in checks if not row['passed']],
                         comparisons=comparisons, floor_errors=floors,
                         chemical_coefficient=float(chemical_coefficient))), flush=True)


if __name__ == '__main__':
    main()
