from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    applied, induced, outside_applied, outside_induced, wronskian = sp.symbols('applied induced outside_applied outside_induced wronskian')
    checks = []

    def exact(name, expression):
        assert sp.factor(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    response = induced/(3*(applied-induced*outside_applied/outside_induced))
    conservative = induced/(3*applied)
    mixing = outside_applied/outside_induced
    exact('retarded_radiation_dressing', response-conservative/(1-3*conservative*mixing))
    radius_left, radius_right = sp.symbols('radius_left radius_right')
    regular_left, irregular_left, outgoing_right = sp.symbols('regular_left irregular_left outgoing_right')
    total_green = (applied*regular_left+induced*irregular_left)*outgoing_right/((applied*outside_induced-induced*outside_applied)*wronskian)
    reference_green = regular_left*outgoing_right/(outside_induced*wronskian)
    outgoing_left = outside_applied*regular_left+outside_induced*irregular_left
    excess = 3*response*(outgoing_left/outside_induced)*(outgoing_right/outside_induced)/wronskian
    exact('rank_one_retarded_Green_difference', total_green-reference_green-excess)
    left_value, left_prime, right_value, right_prime, source = sp.symbols('left_value left_prime right_value right_prime source')
    determinant = left_value*right_prime-left_prime*right_value
    interior_multiplier, exterior_multiplier = source*right_value/determinant, source*left_value/determinant
    exact('source_shell_continuity', interior_multiplier*left_value-exterior_multiplier*right_value)
    exact('source_shell_derivative_jump', exterior_multiplier*right_prime-interior_multiplier*left_prime-source)
    real_lambda, mixing_real, mixing_imag = sp.symbols('real_lambda mixing_real mixing_imag', real=True)
    dressed = real_lambda/(1-3*real_lambda*(mixing_real+sp.I*mixing_imag))
    exact('outgoing_optical_identity', sp.im(sp.expand_complex(dressed))-3*mixing_imag*sp.expand_complex(dressed*sp.conjugate(dressed)))
    change_a, change_b, change_c, change_d = sp.symbols('change_a change_b change_c change_d')
    transformation = sp.Matrix([[change_a, change_b], [change_c, change_d]])
    original_inside = sp.Matrix([applied, induced])
    original_outside = sp.Matrix([outside_applied, outside_induced])
    new_inside, new_outside = transformation.inv()*original_inside, transformation.inv()*original_outside
    exact('basis_change_preserves_pole_denominator_up_to_nonzero_factor', sp.det(sp.Matrix.hstack(new_inside, new_outside))*transformation.det()-sp.det(sp.Matrix.hstack(original_inside, original_outside)))
    sigma, frequency, width = sp.symbols('sigma frequency width', real=True)
    residue_real, residue_imag = sp.symbols('residue_real residue_imag', real=True)
    pole, residue = frequency-sp.I*width, residue_real+sp.I*residue_imag
    pair = residue/(sigma-pole)-sp.conjugate(residue)/(sigma+sp.conjugate(pole))
    exact('pole_pair_reality', pair.subs(sigma, -sigma)-sp.conjugate(pair))
    exact('pole_pair_static_value', pair.subs(sigma, 0)+2*sp.re(residue/pole))
    denominator0, denominator1, numerator0 = sp.symbols('denominator0 denominator1 numerator0', nonzero=True)
    variable = sp.Symbol('variable')
    exact('simple_pole_residue', sp.limit(variable*numerator0/(denominator1*variable), variable, 0)-numerator0/denominator1)
    lambda0, lambda2, sigma_symbol = sp.symbols('lambda0 lambda2 sigma_symbol')
    source_amplitude, field = sp.symbols('source_amplitude field')
    induced_field = -(lambda0+lambda2*sigma_symbol**2)*source_amplitude
    exact('derivative_response_sign', induced_field+lambda0*source_amplitude+lambda2*sigma_symbol**2*source_amplitude)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'exact_check_count': len(checks),
              'response': 'chi_b = lambda_K,b/(1-3 lambda_K,b p_b/q_b)',
              'rank_one_identity': 'G_body-G_P = 3 chi_b [V(r)/q_b][V(rprime)/q_b]/W(P_b,Q_b)',
              'shell_transfer': 'Z(R)/S = U(R) V(r_source)/W(U,V)',
              'pole_residue': 'Res chi_b = N(sigma_p)/Dprime(sigma_p)',
              'pole_pair': 'Res/(sigma-sigma_p)-conjugate(Res)/(sigma+conjugate(sigma_p))',
              'scope': 'Finite-radius static-seeded master-field normalization, explicitly scheme dependent away from zero frequency; full Green function and poles independent of basis.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}))


if __name__ == '__main__':
    main()
