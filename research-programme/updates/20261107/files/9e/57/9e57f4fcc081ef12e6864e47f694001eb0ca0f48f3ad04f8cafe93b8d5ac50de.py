from matched_weak import *


def main():
    modest()
    folder = ROOT / 'results/mass-weak-projection'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    step = .001
    for temperature in [.00014534465573404461, .00045962015785263325]:
        values = [np.zeros((4, 4)) for index in range(4)]
        direct_average = np.zeros((4, 4))
        electron_nodes = []
        for meridian, weight in inherited.gas_rule(temperature, 6, 6):
            for azimuth in np.arange(8) * np.pi / 4:
                electron_nodes.append((np.array([meridian[0] * math.cos(azimuth),
                                                meridian[0] * math.sin(azimuth), meridian[2]]), weight / 8))
        for velocity, measure in electron_nodes:
            gamma_squared = 1 / (1 - velocity @ velocity)
            momentum = math.sqrt(gamma_squared) * velocity
            score = normalized_mass_score(momentum @ momentum, temperature)
            base = born_weak(temperature, .1, velocity, temperature)
            def fixed_velocity(displacement):
                return born_weak(temperature, .1, velocity, temperature, mass=math.sqrt(1 + displacement))
            def changed_velocity(displacement):
                tangent = -velocity / (2 * gamma_squared)
                return born_weak(temperature, .1, velocity + displacement * tangent, temperature)
            def physical_family(displacement):
                mass = math.sqrt(1 + displacement)
                changed = momentum / math.sqrt(1 + displacement + momentum @ momentum)
                return (mass_reweight(momentum @ momentum, temperature, displacement)
                        * born_weak(temperature, .1, changed, temperature, mass=mass))
            def derivative(function, width):
                return (-function(2 * width) + 8 * function(width) - 8 * function(-width) + function(-2 * width)) / (12 * width)
            fixed = derivative(fixed_velocity, step)
            canonical = derivative(changed_velocity, step)
            population = score * base
            for total, value in zip(values, [base, fixed, canonical, population]):
                total += measure * value
            direct_average += measure * derivative(physical_family, step / 2)
        derived = sum(values[1:])
        null = np.array([1., 0., 0., 1.])
        checks.extend([
            check('Gas weak mass derivative equals normalized fixed-p family T=' + str(temperature),
                  relative(derived, direct_average), 3e-8),
            check('Common energy null survives differentiated gas average T=' + str(temperature),
                  np.linalg.norm(derived @ null) / np.linalg.norm(derived), 1e-8),
            dict(name='Population term matters for weak derivative T=' + str(temperature),
                 passed=bool(np.linalg.norm(values[3]) / np.linalg.norm(derived) > .05)),
            dict(name='Canonical chain term matters for weak derivative T=' + str(temperature),
                 passed=bool(np.linalg.norm(values[2]) / np.linalg.norm(derived) > .05))])
        rows.append(dict(temperature=temperature, relative_derivative_error=relative(derived, direct_average),
                         fixed_velocity_norm=float(np.linalg.norm(values[1])),
                         canonical_norm=float(np.linalg.norm(values[2])),
                         population_norm=float(np.linalg.norm(values[3])),
                         total_norm=float(np.linalg.norm(derived)),
                         omission_population_relative_error=float(np.linalg.norm(values[3]) / np.linalg.norm(derived))))
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), rows=rows,
           scope='Scalar mass family independently tests weak observable, kernel, flux and population derivatives, not the genuine full thermal vertex.'), __file__)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
