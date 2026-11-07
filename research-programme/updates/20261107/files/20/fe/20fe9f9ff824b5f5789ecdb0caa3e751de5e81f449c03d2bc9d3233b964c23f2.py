from leading_pair import *
from stable_pair import coefficients
from increment_emitting_geometry import IncrementEmittingGeometry


def main():
    modest()
    folder = ROOT / 'results/leading-compton-pair'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], [ROOT / 'leading_pair.py', BRANCH / 'mixed-bath-transport-20261007/stable_pair.py']
    for model in ['heavy', 'cold']:
        geometry = IncrementEmittingGeometry(model, model + '-ir96-integrated-6400')
        inputs.append(geometry.source)
        for expansion in [.05, 1., math.log(10)]:
            theta = geometry.at(expansion)['theta']
            profile = geometry.profiles(expansion)
            gas = float(geometry.temperature(expansion))
            first = np.geomspace(.0001, 20., 57)
            second = first * (1 + .02 * np.sin(np.arange(len(first))))
            gamma = 1 + theta * np.linspace(.1, 9., len(first))
            initial = geometry.basis.evaluate(first) @ profile
            final = geometry.basis.evaluate(second) @ profile
            derived = np.asarray(leading_coefficients(first, second, initial, final, gas, theta, gamma))
            errors = []
            for amplitude in [1e-5, 1e-6, geometry.heat]:
                actual = np.asarray(coefficients(first, second, initial, final, amplitude, amplitude * gas, theta, gamma)[:3]) / amplitude
                error = float(np.max(abs(actual - derived)) / max(np.max(abs(derived)), 1e-100))
                errors.append(error)
                checks.append(check(model + ' physical pair derivative s=' + str(expansion) + ' chi=' + str(amplitude),
                                    error, max(50 * amplitude, 1e-8)))
            checks.append(dict(name=model + ' first-order pair convergence s=' + str(expansion),
                               passed=errors[1] < .2 * errors[0] and errors[2] < .02 * errors[1], errors=errors))
            rows.append(dict(model=model, expansion=expansion, errors=errors))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        rows=rows, actual_emitting_profiles=True, number_projection_applied=False,
        result='Closed leading-heat finite-shift Compton pair coefficients replace repeated tiny differences; no angular or diffusion approximation added.'), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
