from dirac_amplitude import *


def boost_vector(vector, velocity):
    velocity = mp.matrix([mp.mpf(str(value)) for value in velocity])
    speed2 = sum(value ** 2 for value in velocity)
    gamma = 1 / mp.sqrt(1 - speed2)
    product = sum(vector[index + 1] * velocity[index] for index in range(3))
    spatial = mp.matrix(list(vector)[1:]) + ((gamma - 1) * product / speed2 - gamma * vector[0]) * velocity
    return mp.matrix([gamma * (vector[0] - product), *spatial])


def main():
    modest()
    mp.mp.dps = 80
    folder = ROOT / 'results/boosted-amplitude'
    folder.mkdir(parents=True, exist_ok=False)
    sample = event(.00045962015785263325, .1, [.7, .2, -.3], [-.3, .5, .6])
    original = tensor_for_event(sample)
    reference = float(np.sum(abs(original) ** 2) / 4)
    checks, rows = [], []
    for velocity in [[.01, .02, -.03], [.3, -.4, .2], [0., .7, 0.]]:
        photons = [boost_vector(momentum, velocity) for momentum in sample['photons']]
        directions = [mp.matrix(list(momentum)[1:]) / momentum[0] for momentum in photons]
        boosted = dict(initial=boost_vector(sample['initial'], velocity), final=boost_vector(sample['final'], velocity),
            photons=photons, directions=directions, frames=[frame(direction) for direction in directions])
        amplitude = tensor_for_event(boosted)
        actual = float(np.sum(abs(amplitude) ** 2) / 4)
        checks.append(check('Invariant spin/polarization sum velocity=' + str(velocity), abs(actual / reference - 1), 1e-12))
        for leg in range(3):
            ward = tensor_for_event(boosted, ward=leg)
            error = float(linalg.norm(ward.ravel()) / linalg.norm(amplitude.ravel()))
            checks.append(check('Moving-electron Ward identity leg=' + str(leg) + ' velocity=' + str(velocity), error, 1e-45))
        rows.append(dict(velocity=velocity, squared=actual, reference=reference))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        moving_initial_electrons_tested=True, photon_basis_regauged_transverse=True,
        thermal_average_not_replaced_by_single_boost=True), __file__, [ROOT / 'dirac_amplitude.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
