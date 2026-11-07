from observer_common import *
import sympy as symbolic


def main():
    modest()
    folder = ROOT / 'results/scaled-variable-identities'
    folder.mkdir(parents=True, exist_ok=False)
    heat, moment, first, second, shift_first, shift_second, amplitude, shape_amplitude, slip, source_first, source_second = symbolic.symbols('chi n a b d e theta y eta w0 w1')
    number = symbolic.Matrix([[1, moment]])
    thermal = symbolic.Matrix([first, second])
    complement = symbolic.Matrix([-moment, 1])
    shift = symbolic.Matrix([shift_first, shift_second])
    source = symbolic.Matrix([source_first, source_second])
    normalization = (number * thermal)[0]
    projector = symbolic.eye(2) - thermal * number / normalization
    physical = thermal * amplitude + heat * source
    dilation = thermal + heat * shift
    temperature = (number * physical)[0] / (number * dilation)[0]
    direct_shape = physical - dilation * temperature
    scaled_shape = heat * (projector * source - temperature * projector * shift)
    transform = symbolic.Matrix([[first, -heat * moment, 0], [second, heat, 0], [1, 0, heat]])
    inverse = transform.inv()
    identities = [
        ('Temperature and shape decomposition is exactly reconstructible', direct_shape + dilation * temperature - physical),
        ('Direct small-shape expression equals subtractive definition', scaled_shape - direct_shape),
        ('Scaled shape has the same number-free definition', number * scaled_shape),
        ('Complement carries no number moment', number * complement),
        ('Temperature projector annihilates only its template', projector * thermal),
        ('Projector is idempotent', projector * projector - projector),
        ('Combined photon-shape and gas-slip transform is invertible', inverse * transform - symbolic.eye(3)),
        ('Transform determinant is chi squared times the thermal number moment', symbolic.Matrix([transform.det() - heat ** 2 * normalization]))]
    checks = [dict(name=name, passed=all(symbolic.simplify(value) == 0 for value in expression)) for name, expression in identities]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        assumptions=['chi is nonzero; the Planck-only chi=0 control is handled separately', 'N q_T is nonzero'],
                        determinant=str(symbolic.factor(transform.det())),
                        unchanged_physical_degrees_of_freedom=True,
                        evolution_not_yet_implemented_in_scaled_coordinates=True,
                        equations={'split': 'X=q_T theta+chi V y; t_gas=theta_0+chi eta',
                                   'shape': 'S=chi[P_T W-Theta_dist P_T q_1]',
                                   'evolution': 'M P z_prime=(L P-M P_prime)z; P_prime=0 for fixed q_T and chi'},
                        scope='Exact change of variables and stable readout identity, not a new constitutive law or a repaired time-accuracy claim.'), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    main()
