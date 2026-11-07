import argparse
from gould_overlap import *
from log_rectangular import logarithmic_rule


def sampled(spectra, tests, theta, seed_order, radial, floor=1e-6):
    output = np.zeros((spectra.basis.count + 2, 4))
    prefactor = 4 * weak.source.ALPHA * theta**2 / (3 * np.pi * I3)
    for anchor, anchor_weight in incoming_rule(seed_order, 1e-5, 24.):
        def integrate_piece(lower, upper, inverse, spontaneous):
            if upper <= lower:
                return
            soft, weights = logarithmic_rule(radial, lower, upper)
            hard = np.full_like(soft, anchor) if inverse else anchor - soft
            seed = hard + soft if inverse else np.full_like(soft, anchor)
            left = tests.evaluate(soft) + tests.evaluate(hard) - tests.evaluate(seed)
            left[:, 0] = 0.
            left[:, 1] = 1 / spectra.basis.norms[0]
            left[:, 2] = -spectra.basis.mean / spectra.basis.norms[1]
            right = spectra.functions(soft)[:, 1:] + spectra.functions(hard)[:, 1:] - spectra.functions(seed)[:, 1:]
            density = .5 * prefactor * anchor_weight * weights * seed**4 * gould(soft / seed)
            density /= np.expm1(seed) * (-np.expm1(-hard)) * soft
            if inverse:
                density /= -np.expm1(-soft)
            elif not spontaneous:
                density /= np.expm1(soft)
            output[:-1] -= (left.T * density) @ right
        integrate_piece(floor, anchor / 2, False, True)
        boundaries = sorted({floor, anchor / 2, anchor, 60.,
            *[scale for scale in [.1, .5, 1., 2., 5., 10., 20., 40.] if floor < scale < 60.]})
        for lower, upper in zip(boundaries[:-1], boundaries[1:]):
            if upper <= anchor / 2 * (1 + 1e-14):
                integrate_piece(lower, upper, False, False)
            if upper <= anchor * (1 + 1e-14):
                integrate_piece(lower, upper, True, False)
    return output


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-run', required=True)
    parser.add_argument('--name', required=True)
    arguments = parser.parse_args()
    source_folder = ROOT / 'runs' / arguments.source_run
    source = json.loads((source_folder / 'status.json').read_text())
    assert source['epoch_fraction'] == .5
    parent = json.loads((PARENT / 'runs' / source['arguments']['source_run'] / 'status.json').read_text())
    folder = ROOT / 'controls' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(source['epoch_fraction'])
    tests = TestFunctions(spectra.basis)
    low = sampled(spectra, tests, source['temperature'], parent['configuration']['seed_order'], source['arguments']['radial'])
    fine_path = ROOT / 'overlaps/midpoint-gould48/overlap.npz'
    fine = dict(np.load(fine_path))['joined_new_domain']
    projected = dict(np.load(source_folder / 'source.npz'))
    repaired = projected['total'] - low + fine
    energy_error = float(np.max(abs(repaired[0] - projected['total'][0])))
    checks = [
        dict(name='Leading sampled control and exact high-order addback are finite', passed=np.isfinite(repaired).all()),
        dict(name='Control-variate addback preserves independent energy and gas rows', value=energy_error,
             passed=energy_error == 0 and np.array_equal(repaired[-1], projected['total'][-1])),
        dict(name='No source test or high-frequency component was discarded', passed=repaired.shape == (98, 4)),
    ]
    np.savez(folder / 'source.npz', total=repaired, raw=projected['total'], sampled_leading=low,
             accurate_leading=fine, remainder=projected['total'] - low,
             mass=projected['mass'], chemical=projected['chemical'], temperature=projected['temperature'],
             number=projected['chemical'] @ repaired[1:-1])
    finish(folder, dict(checks=checks, arguments=vars(arguments),
        estimator='Numerically integrate full-minus-leading and add independent leading result; no discarded modes.',
        convergence_required_before_use=True, leading_angular_integral_analytic=True,
        moving_recoil_remainder_retained=True, new_parent_action=False,
        full_parent_feedback_applied=False), __file__,
        [*spectra.inputs, source_folder / 'status.json', source_folder / 'source.npz', fine_path, fine_path.parent / 'status.json'])
    print(json.dumps(dict(name=arguments.name, checks=len(checks),
        failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
