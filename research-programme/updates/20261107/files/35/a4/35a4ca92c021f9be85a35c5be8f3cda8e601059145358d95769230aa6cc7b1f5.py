from emission_angular_common import *


def main():
    modest()
    folder = ROOT / 'results/mixed-reaction-quadrature'
    folder.mkdir(parents=True, exist_ok=False)
    coarse = ROOT / 'banks/bose-mixed104-q300-180'
    fine = ROOT / 'banks/bose-mixed104-q420-240'
    inputs = [coarse / 'status.json', fine / 'status.json']
    checks = []
    for path in sorted(fine.glob('*.npz')):
        other = coarse / path.name
        inputs.extend([path, other])
        with np.load(path) as saved, np.load(other) as reference:
            for degree in range(5):
                name = 'mixed_' + str(degree)
                error = linalg.norm(saved[name] - reference[name]) / max(linalg.norm(saved[name]), 1e-100)
                checks.append(check(path.stem + ' mixed reaction quadrature l=' + str(degree), error, .002))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        maximum=max(row['value'] for row in checks), operator_norm_only=True,
        cutoff_independent_or_polarized_transport_not_implied=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], maximum=max(row['value'] for row in checks))), flush=True)


if __name__ == '__main__':
    main()
