from mixed_common import *
from build_mixed_bank import background_profile


def main():
    modest()
    folder = ROOT / 'results/isotropic-reduction'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    events = grid.event_geometry(4.596201578526332e-4, 6)
    selection = np.linspace(0, len(events['weight']) - 1, 17).astype(int)
    events = {key: value[selection] for key, value in events.items()}
    initial = np.array([0., 0., 1.])
    initial_frame = grid.prior.frames(initial)
    recoil_extra = np.linspace(.001, .3, len(selection))
    identity = np.broadcast_to(np.eye(2), (len(selection), 2, 2))
    first_loss, correction = grid.fano_adjoint(events['jones'], events['cosine'], identity)
    first_loss = first_loss + recoil_extra[:, None, None] * correction
    second_loss = grid.fano_gain(events['jones'], events['cosine'], recoil_extra, identity)
    for degree in range(9):
        axes = grid.angular.AngularKernel(degree + 2, 2 * (degree + 2))
        modes = 2 if degree < 2 else 4
        left = np.zeros((modes, modes, len(selection)), complex)
        right = np.zeros_like(left)
        for axis, weight in zip(axes.directions, axes.weights):
            source, _ = grid.modal_tensors(initial, axis, degree)
            target, _ = grid.modal_tensors(events['final_direction'], axis, degree)
            source = initial_frame.T @ source @ initial_frame
            target = events['final_frame'].swapaxes(-1, -2) @ target @ events['final_frame']
            left_pair = (source[:, None] @ first_loss + first_loss @ source[:, None]) / 2
            right_pair = (target @ second_loss + second_loss @ target) / 2
            left += weight * np.einsum('aij,bnji->abn', source, left_pair)
            right += weight * np.einsum('anij,bnji->abn', target, right_pair)
        expected = (1 + events['cosine'] ** 2 + recoil_extra) / (2 * degree + 1)
        diagonal = np.eye(modes)[:, :, None] * expected
        error = float(max(np.max(abs(left - diagonal)), np.max(abs(right - diagonal))))
        checks.append(dict(name='Full anticommutator angular loss reduces correctly degree' + str(degree),
                           passed=error < 1e-9, value=error))
    systems = [RefinedSystem(model, 24, 8) for model in ['heavy', 'cold']]
    basis = systems[0].basis
    frequencies = np.unique(np.r_[basis.nodes, np.geomspace(basis.minimum, basis.maximum, 500)])
    values = basis.evaluate(frequencies)
    planck = 1 / np.expm1(frequencies)
    for system in systems:
        minimum, maximum = 1., 0.
        for expansion in np.linspace(0., system.geometry.thermal.end, 101):
            profile, shift, heat = background_profile(system, expansion)
            relative = (1 + planck) * heat * (values @ profile)
            minimum = min(minimum, float(min(1 + relative)))
            maximum = max(maximum, float(max(abs(relative))))
            assert 1 + shift > 0
        checks.append(dict(name=system.model + ': retained scalar background occupation positive over tested frequency-time grid',
                           passed=minimum > 0, minimum_planck_ratio=minimum, maximum_fractional_distortion=maximum))
        rows.append(dict(model=system.model, theta_start=system.background(0.)['theta'],
                         heat=system.background(0.)['heat'], initial_profile_number=float(basis.number @ system.geometry.profiles(0.))))
    checks.append(dict(name='Common reference electron temperature for both event banks',
                       passed=rows[0]['theta_start'] == rows[1]['theta_start']))
    finish(folder, dict(checks=checks, all_checks_passed=all(row['passed'] for row in checks), count=len(checks), rows=rows,
                        positivity_is_sampled_not_global_analytic_bound=True), __file__,
           [ROOT / 'build_mixed_bank.py', GRID / 'grid_common.py', *[system.geometry.source for system in systems]])
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
