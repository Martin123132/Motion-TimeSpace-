from nonlocal_dc import *
from batched_real import intensity_batch
import polarized_source as source


def main():
    modest()
    folder = ROOT / 'results/exact-amplitude-limit'
    folder.mkdir(parents=True, exist_ok=False)
    fractions = np.array([.01, .1, .3, .45])
    rows = []
    directions = list(source.angular_nodes(4))
    prefactor = 3 * source.ALPHA / (128 * np.pi**3)
    for energy in [1e-3, 1e-4, 1e-5]:
        integrated = np.zeros(len(fractions))
        soft = energy * fractions
        for hard_direction, hard_weight in directions:
            for soft_direction, soft_weight in directions:
                intensity, photons, final, hard, denominator = intensity_batch(
                    energy, soft, hard_direction, soft_direction)
                integrated += hard_weight * soft_weight * prefactor * hard * soft / (energy * denominator) * intensity
        expected = 4 * source.ALPHA / (3 * np.pi) * energy**2 * gould(fractions) / soft
        rows.append(dict(energy=energy, ratios=(integrated / expected).tolist(),
                         maximum_relative_remainder=float(np.max(abs(integrated / expected - 1)))))
    checks = [
        check('Exact six-diagram angular integral approaches Gould at all tested split fractions',
              rows[-1]['maximum_relative_remainder'], 1e-4),
        dict(name='Recoil remainder decreases with incoming energy instead of being fitted away',
             passed=rows[-1]['maximum_relative_remainder'] < rows[0]['maximum_relative_remainder'] * .011)]
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), rows=rows,
           fractions=fractions.tolist(), normalization_independent_of_local_emission_matrix=True),
           __file__)
    print(json.dumps(dict(rows=rows, failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
