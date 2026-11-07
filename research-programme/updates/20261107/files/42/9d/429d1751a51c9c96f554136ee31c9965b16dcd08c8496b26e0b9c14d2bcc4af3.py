import mpmath as mp
from finite_shift_soft_pole import *


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/finite-shift-cold-limit'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [ROOT / 'finite_shift_soft_pole.py'], []
    invariants = np.geomspace(1e-20, 2., 31)
    actual = cusp_array(invariants)
    expected = []
    for invariant in invariants:
        exact = mp.mpf(str(invariant))
        speed = mp.sqrt(exact * (2 + exact)) / (1 + exact)
        expected.append(float(2 * mp.mpf(str(ALPHA)) / mp.pi * (mp.atanh(speed) / speed - 1)))
    checks.append(check('Stable invariant-current coefficient matches independent70-digit formula', np.max(abs(actual / expected - 1)), 1e-12))
    basis = ConsistentBasis(count=104, quadrature=700, minimum=1e-5, maximum=60., pivot=.1)
    theta = 4.5962015785263325e-9
    blocks, names, discarded = all_blocks(basis, theta, 4)
    for degree, block in enumerate(blocks):
        source = ROOT / 'banks/polarized-singular104' / ('pole-' + str(degree) + '.npz')
        inputs.append(source)
        with np.load(source) as saved:
            reference = saved['real_coefficient']
            mass = saved['mass']
        error = linalg.norm(block - reference) / linalg.norm(reference)
        checks.append(check('Finite-shift polarized soft matrix reaches cold limit l=' + str(degree), error, 1e-4))
        template = np.r_[basis.temperature, np.zeros((len(names[degree]) - 1) * basis.count)]
        reference_moment = float(-template @ reference @ template / (template @ mass @ template))
        moment = float(-template @ block @ template / (template @ mass @ template))
        checks.append(check('Temperature moment reaches independent pole l=' + str(degree), abs(moment - reference_moment) / max(1., abs(reference_moment)), 1e-5))
        rows.append(dict(degree=degree, matrix_error=error, temperature_moment=moment, reference=reference_moment))
    np.savez_compressed(folder / 'limit.npz', theta=theta, **{'pole_' + str(degree): block for degree, block in enumerate(blocks)})
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        theta=theta, discarded_weight=discarded, this_is_a_limit_test_not_a_new_parent_model=True), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
