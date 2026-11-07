from nonlocal_common import *
from resolved_redistribution import incoming_transform
import polarized_source as source


def moments(temperature, order):
    powers = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    result = np.zeros(len(powers))
    for velocity, gas_weight in inherited.gas_rule(temperature, order, order):
        transform, bath, incoming_doppler = incoming_transform(velocity)
        for direction, angular_weight in source.angular_nodes(order):
            ratio = incoming_doppler * source.dot(bath, np.r_[1., direction])
            conductance = gas_weight * (1 - velocity[2]) * 3 / (16 * np.pi)
            conductance *= angular_weight * (1 + direction[2]**2) / ratio
            result += conductance * np.expm1(powers * math.log(ratio))
    return powers, result


def main():
    modest()
    folder = ROOT / 'results/soft-compton-moments'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    for temperature in [.000045962015785263324, .00014534465573404461, .00045962015785263325]:
        powers, coarse = moments(temperature, 4)
        powers, fine = moments(temperature, 6)
        checks.append(check('Exact soft Thomson Mellin moments angular/gas refinement T=' + str(temperature),
                            relative(coarse, fine), 1e-5))
        checks.append(check('Soft detailed-balance Mellin symmetry T=' + str(temperature),
                            max(abs(fine[index] - fine[7 - index]) for index in range(8)) / np.linalg.norm(fine), 1e-9))
        expected = powers * (powers + 1) * temperature
        checks.append(check('Leading Kompaneets polynomial is recovered rather than assumed T=' + str(temperature),
                            relative(fine, expected), .006))
        rows.append(dict(temperature=temperature, powers=powers.tolist(), eigenvalues=fine.tolist(),
                         eigenvalues_divided_by_temperature=(fine / temperature).tolist(),
                         refinements=relative(coarse, fine)))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
           rows=rows, recoil_free_soft_operator_exact_in_velocity=True,
           full_finite_frequency_collision_bound=False), __file__)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
