from angular232 import *
from preflight232 import axis_rule


def explicit_radial(frequency):
    return np.array([frequency, frequency**2 / (1 + frequency), frequency**3 / (1 + frequency)**2])


def main():
    modest()
    config = protocol()
    frozen = read(ROOT / 'rotation-configuration.json')
    assert digest(ROOT / 'real_rotation232.py') == frozen['script_sha256']
    checks, examples = [], []
    axes, weights = axis_rule(10)
    direction = np.array([.3, -.4, math.sqrt(.75)])
    for probe in config['probes']:
        parameters = inherited.source.context(probe['temperature'], probe['lab_cosine'], probe['velocity'], probe['temperature'])
        energy, hard_direction = parameters['energy'], parameters['hard_direction']
        transform = parameters['transform']
        incident = transform @ np.array([energy, 0., 0., energy])
        for sign in (1., -1.):
            soft_values = sign * probe['temperature'] * np.array([1e-5, .01, .1])
            for degree in (0, 1, 2):
                lift = AngularWeak(degree)
                density, actual, audit = lift.event_products(parameters, soft_values, direction)
                for index, soft in enumerate(soft_values):
                    hard = (energy - soft - energy * soft * (1 - direction[2])) / (1 + energy * (1 - hard_direction[2]) - soft * (1 - direction @ hard_direction))
                    hard_photon = transform @ np.r_[hard, hard * hard_direction]
                    soft_photon = transform @ np.r_[abs(soft), abs(soft) * direction]
                    recoil = np.array([0., 0., energy]) - hard * hard_direction - soft * direction
                    recoil_energy = recoil @ recoil / (math.sqrt(1 + recoil @ recoil) + 1)
                    electron = transform @ np.r_[recoil_energy, recoil]
                    tests = np.zeros((len(axes), 4))
                    for four, coefficient in [(incident, -1.), (hard_photon, 1.), (soft_photon, sign)]:
                        orientation = four[1:] / np.linalg.norm(four[1:])
                        tests[:, :3] += coefficient * special.eval_legendre(degree, axes @ orientation)[:, None] * explicit_radial(four[0] / probe['temperature'])
                    if degree == 0:
                        tests[:, -1] = electron[0] / probe['temperature']
                    if degree == 1:
                        tests[:, -1] = axes @ electron[1:] / probe['temperature']
                    direct = (tests.T * weights) @ tests
                    check(checks, f'{probe["label"]}:{sign}:l{degree}:{index}: three-leg independent axis quadrature', relative(actual[index], direct), 1e-10)
                    if degree == 1:
                        wrong_momentum = (hard_photon[0] * hard_direction + sign * soft_photon[0] * direction - incident[0] * np.array([0., 0., 1.]) + electron[1:]) / probe['temperature']
                        error = float(np.linalg.norm(wrong_momentum))
                        check(checks, f'{probe["label"]}:{sign}:{index}: mixing rest directions with lab energies detected', int(error < 1e-7), 0)
                        examples.append(dict(probe=probe['label'], sign=sign, soft_index=index, wrong_frame_momentum_residual=error))
    assert not (ROOT / 'results/real-rotation.json').exists()
    report = dict(stage=232, state='complete', finished_at=now(), qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], examples=examples,
        scope='Independent on-shell three-leg geometry and explicit rotation quadrature, with wrong-frame negative controls')
    write(ROOT / 'results/real-rotation.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'])), flush=True)


if __name__ == '__main__':
    main()
