from grid_common import *


def main():
    modest()
    folder = ROOT / 'results/high-angular-blocks'
    assert not folder.exists()
    source = ROOT / 'banks/main-96/status.json'
    theta = json.loads(source.read_text())['theta']
    checks, rows = [], []
    for temperature in [theta, 10 * theta]:
        events = event_geometry(temperature, 3)
        for degree in range(5, 9):
            first, second, names = angular_correlations(events, degree)
            finer_first, finer_second, _ = angular_correlations(events, degree, extra_axis=2)
            difference = float(max(np.max(abs(first - finer_first)), np.max(abs(second - finer_second))))
            recoil = 1 / (1 + temperature * 8 * events['incident'] * (1 - events['cosine']))
            extra = (1 - recoil) ** 2 / recoil
            cross = first + extra[None, None, :] * second
            singular = np.linalg.svd(cross.transpose(2, 0, 1), compute_uv=False)[:, 0]
            self_term = (1 + events['cosine'] ** 2 + extra) / (2 * degree + 1)
            violation = float(max(np.max(singular - self_term), 0.))
            target = self_term * special.eval_legendre(degree, events['final_direction'][:, 2])
            scalar_error = float(np.max(abs(cross[0, 0] - target)))
            checks.extend([
                dict(name=str(temperature) + ':degree' + str(degree) + ': independently refined axis quadrature',
                     passed=difference < 1e-9, value=difference),
                dict(name=str(temperature) + ':degree' + str(degree) + ': exact scalar addition theorem',
                     passed=scalar_error < 1e-9, value=scalar_error),
                dict(name=str(temperature) + ':degree' + str(degree) + ': physical pair contraction',
                     passed=violation < 1e-9, value=violation)])
            rows.append(dict(theta=temperature, degree=degree, names=names,
                             axis_refinement_error=difference, scalar_addition_error=scalar_error,
                             contraction_violation=violation))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, completes_independent_axis_checks_through_degree8=True), __file__, [source])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
