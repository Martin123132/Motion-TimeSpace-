import sympy as symbolic
import mpmath as mp
from bose_reaction import *
from reaction_geometry import ReactionGeometry


def main():
    modest()
    mp.mp.dps = 70
    folder = ROOT / 'results/bose-reaction-hessian'
    folder.mkdir(parents=True, exist_ok=False)
    occupations = symbolic.symbols('n0:3')
    perturbations = symbolic.symbols('f0:3')
    backgrounds = symbolic.symbols('B0:3')
    heat, wave = symbolic.symbols('chi epsilon')
    weights = [value * (1 + value) for value in occupations]
    shifted = [occupations[index] + weights[index] * (heat * backgrounds[index] + wave * perturbations[index]) for index in range(3)]
    forward = shifted[0] * (1 + shifted[1]) * (1 + shifted[2]) - (1 + shifted[0]) * shifted[1] * shifted[2]
    simplified = shifted[0] + shifted[0] * shifted[1] + shifted[0] * shifted[2] - shifted[1] * shifted[2]
    checks = [dict(name='Bose cubic terms cancel exactly', passed=symbolic.expand(forward - simplified) == 0)]
    mixed = symbolic.diff(forward, heat, wave).subs({heat: 0, wave: 0})
    expected = weights[0] * (weights[1] * backgrounds[1] + weights[2] * backgrounds[2]) * perturbations[0]
    expected += weights[1] * (weights[0] * backgrounds[0] - weights[2] * backgrounds[2]) * perturbations[1]
    expected += weights[2] * (weights[0] * backgrounds[0] - weights[1] * backgrounds[1]) * perturbations[2]
    checks.append(dict(name='Exact mixed background-wave Bose derivative', passed=symbolic.expand(mixed - expected) == 0))
    first_exp, second_exp = symbolic.symbols('u v', positive=True)
    planck = {occupations[0]: 1 / (first_exp * second_exp - 1), occupations[1]: 1 / (first_exp - 1), occupations[2]: 1 / (second_exp - 1)}
    equilibrium_forward = occupations[0] * (1 + occupations[1]) * (1 + occupations[2])
    linear = symbolic.diff(forward, wave).subs({heat: 0, wave: 0})
    identity = symbolic.factor((linear - equilibrium_forward * (perturbations[0] - perturbations[1] - perturbations[2])).subs(planck))
    checks.append(dict(name='Planck detailed-balance event difference', passed=identity == 0))
    checks.append(dict(name='No photon-number invariant imposed', passed=symbolic.simplify(1 - 1 - 1) == -1))
    rows, inputs = [], []
    for model in ['heavy', 'cold']:
        geometry = ReactionGeometry(model, model + '-reaction104-6400')
        inputs.append(geometry.source)
        for expansion in [.05, 1., math.log(10)]:
            profile = geometry.profiles(expansion)
            frequencies = np.array([[total, total * (1 - fraction), total * fraction]
                for total in [.001, .01, .1, 1., 5., 20.] for fraction in [.001, .1, .5]])
            background = np.stack([geometry.basis.evaluate(frequencies[:, index]) @ profile for index in range(3)], axis=1)
            prediction = mixed_coefficients(frequencies, background)
            exact = []
            for event, field in zip(frequencies, background):
                occupation = [1 / mp.expm1(mp.mpf(float(value))) for value in event]
                weight = [value * (1 + value) for value in occupation]
                shifted = [occupation[index] + mp.mpf(float(geometry.heat)) * weight[index] * mp.mpf(float(field[index])) for index in range(3)]
                normalization = occupation[0] * (1 + occupation[1]) * (1 + occupation[2])
                finite = [weight[0] * (1 + shifted[1] + shifted[2]), weight[1] * (shifted[0] - shifted[2]), weight[2] * (shifted[0] - shifted[1])]
                unshifted = [weight[0] * (1 + occupation[1] + occupation[2]), weight[1] * (occupation[0] - occupation[2]), weight[2] * (occupation[0] - occupation[1])]
                exact.append([float((finite[index] - unshifted[index]) / (mp.mpf(float(geometry.heat)) * normalization)) for index in range(3)])
            error = float(np.max(abs(np.array(exact) - prediction)) / max(np.max(abs(prediction)), 1e-100))
            checks.append(check(model + ' mixed Bose derivative at physical heat s=' + str(expansion), error, 1e-11))
            rows.append(dict(model=model, expansion=expansion, relative_error=error))
        frequencies = np.array([[total, total * (1 - fraction), total * fraction]
            for total in [.001, .1, 1., 5., 20.] for fraction in [.001, .1, .5]])
        thermal_coefficients = mixed_coefficients(frequencies, frequencies)
        second_thermal = frequencies ** 2 / np.tanh(frequencies / 2) - 2 * frequencies
        thermal_identity = np.sum(thermal_coefficients * frequencies, axis=1) + second_thermal[:, 0] - second_thermal[:, 1] - second_thermal[:, 2]
        scale = np.maximum(1., np.sum(abs(thermal_coefficients * frequencies), axis=1))
        checks.append(check(model + ' curved Planck-family mixed thermal identity', np.max(abs(thermal_identity) / scale), 1e-10))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        arithmetic_decimal_places=70, exact_for_retained_quadratic_Bose_factor=True,
        electron_recoil_and_polarization_not_inferred=True,
        scalar_rate_extension='Frozen reference-temperature correction only; arbitrary nonequilibrium derivative of its phenomenological rate is not supplied.'), __file__,
        [*inputs, ROOT / 'bose_reaction.py', ROOT / 'gould_angles.py', ROOT / 'reaction_geometry.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
