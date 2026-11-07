import sympy as sp
from kernel_common import *


def main():
    modest()
    folder = ROOT / 'results/derived-form'
    assert not folder.exists()
    checks = []
    def exact(name, expression):
        checks.append(dict(name=name, passed=sp.simplify(sp.expand(expression)) == 0))
    initial_exp, final_exp, electron = sp.symbols('initial_exp final_exp electron', positive=True)
    initial_n, final_n = 1 / (initial_exp - 1), 1 / (final_exp - 1)
    initial_w, final_w = initial_n * (1 + initial_n), final_n * (1 + final_n)
    reverse_electron = electron * final_exp / initial_exp
    conductance = electron * initial_n * (1 + final_n)
    exact('Bose/Juttner equilibrium event weights are reciprocal', conductance - reverse_electron * final_n * (1 + initial_n))
    exact('Induced matrix initial-potential coefficient is negative pair conductance',
          initial_w * (reverse_electron * final_n - electron * (1 + final_n)) + conductance)
    exact('Induced matrix final-potential coefficient is positive pair conductance',
          final_w * (reverse_electron * (1 + initial_n) - electron * initial_n) - conductance)
    left_values = sp.symbols('left0:4', real=True)
    right_values = sp.symbols('right0:4', real=True)
    channel_values = sp.symbols('channel0:8', real=True)
    left = sp.Matrix([[left_values[0], left_values[1] + sp.I * left_values[2]],
                      [left_values[1] - sp.I * left_values[2], left_values[3]]])
    right = sp.Matrix([[right_values[0], right_values[1] + sp.I * right_values[2]],
                       [right_values[1] - sp.I * right_values[2], right_values[3]]])
    channel = sp.Matrix(2, 2, lambda row, column: channel_values[2 * (2 * row + column)] + sp.I * channel_values[2 * (2 * row + column) + 1])
    loss_left = channel.H @ channel
    loss_right = channel @ channel.H
    collision_left = channel.H @ right @ channel - (loss_left @ left + left @ loss_left) / 2
    collision_right = channel @ left @ channel.H - (loss_right @ right + right @ loss_right) / 2
    defect = channel @ left - right @ channel
    exact('Arbitrary complex spin channel conserves the paired photon trace', sp.trace(collision_left + collision_right))
    exact('Arbitrary Hermitian polarized pair dissipates exact channel square',
          sp.trace(left @ collision_left + right @ collision_right + defect.H @ defect))
    initial, final, cosine = sp.symbols('initial final cosine', real=True)
    exact('Dipole Galerkin integrand is a sum of nonnegative squares',
          initial ** 2 + final ** 2 - 2 * cosine * initial * final - (initial - cosine * final) ** 2 - (1 - cosine ** 2) * final ** 2)
    theta, kinetic = sp.symbols('theta kinetic', positive=True)
    momentum = sp.sqrt(theta * kinetic * (2 + theta * kinetic))
    exact('Juttner kinetic-energy radial measure derives from p-squared dp',
          momentum ** 2 * sp.diff(momentum, kinetic) - theta ** sp.Rational(3, 2) * sp.sqrt(kinetic) * (1 + theta * kinetic) * sp.sqrt(2 + theta * kinetic))
    for temperature in [1e-5, 4.596201578526332e-4, .01]:
        nodes, weights = special.roots_genlaguerre(12, .5)
        integral = np.dot(weights, (1 + temperature * nodes) * np.sqrt(2 + temperature * nodes))
        target = special.kve(2, 1 / temperature) / np.sqrt(temperature)
        speeds, normalized = juttner_rule(temperature, 12)
        average_energy = np.dot(normalized, 1 / np.sqrt(1 - speeds ** 2))
        target_energy = special.kve(1, 1 / temperature) / special.kve(2, 1 / temperature) + 3 * temperature
        error = float(max(abs(integral / target - 1), abs(average_energy / target_energy - 1)))
        checks.append(dict(name='Independent Bessel normalization and mean electron energy theta=' + str(temperature),
                           passed=error < 1e-12, value=error, gate=1e-12))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        exact_symbolic_identities=7, physically_derived_reciprocity_and_Galerkin_dissipation=True), __file__)
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
