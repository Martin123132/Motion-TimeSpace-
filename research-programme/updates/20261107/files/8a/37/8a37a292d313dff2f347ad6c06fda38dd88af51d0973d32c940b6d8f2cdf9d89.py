from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
OUTPUT = ROOT / 'results' / 'algebra'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError('Refusing to overwrite executed evidence.')
    OUTPUT.mkdir(parents=True)
    checks = []

    def verify(name, actual, expected=0):
        difference = sym.simplify(actual - expected)
        checks.append({'name': name, 'passed': difference == 0, 'difference': str(difference)})
        if difference != 0:
            raise AssertionError((name, difference))

    amplitude, coupling, quartic, chemical = sym.symbols('amplitude coupling quartic chemical', positive=True)
    radial, phase = sym.symbols('radial phase', real=True)
    fields = (radial, phase)
    modulus_squared = (amplitude + radial)**2 + phase**2
    potential = sym.Rational(3, 4) * coupling * modulus_squared**sym.Rational(2, 3) + quartic * modulus_squared**2 / 4
    background = {radial: 0, phase: 0}
    cubic = {}
    quartic_vertices = {}
    from itertools import product
    for indices in product(range(2), repeat=3):
        cubic[indices] = sym.simplify(sym.diff(potential, *[fields[index] for index in indices]).subs(background))
    for indices in product(range(2), repeat=4):
        quartic_vertices[indices] = sym.simplify(sym.diff(potential, *[fields[index] for index in indices]).subs(background))
    alpha = coupling / amplitude**sym.Rational(8, 3)
    expected_cubic = {0: amplitude * (6 * quartic - 2 * alpha / 9), 2: amplitude * (2 * quartic - 2 * alpha / 3)}
    expected_quartic = {0: 6 * quartic + 10 * alpha / 27, 2: 2 * quartic + 10 * alpha / 9, 4: 6 * quartic - 2 * alpha}
    for indices, expression in cubic.items():
        verify('cubic_' + ''.join(map(str, indices)), expression, expected_cubic.get(sum(indices), 0))
    for indices, expression in quartic_vertices.items():
        verify('quartic_' + ''.join(map(str, indices)), expression, expected_quartic.get(sum(indices), 0))

    frequency, momentum_squared, radial_mass_squared = sym.symbols('omega momentum_squared radial_mass_squared', real=True)
    inverse = sym.Matrix([[frequency**2 - momentum_squared - radial_mass_squared, -2 * sym.I * chemical * frequency], [2 * sym.I * chemical * frequency, frequency**2 - momentum_squared]])
    adjugate = sym.Matrix([[frequency**2 - momentum_squared, 2 * sym.I * chemical * frequency], [-2 * sym.I * chemical * frequency, frequency**2 - momentum_squared - radial_mass_squared]])
    determinant = (frequency**2 - momentum_squared - radial_mass_squared) * (frequency**2 - momentum_squared) - 4 * chemical**2 * frequency**2
    for row in range(2):
        for column in range(2):
            verify(f'inverse_adjugate_{row}_{column}', (inverse * adjugate)[row, column], determinant if row == column else 0)
    verify('determinant', inverse.det(), determinant)
    low_energy, high_energy, separation = sym.symbols('low_energy high_energy separation', positive=True)
    low_squared, high_squared = sym.symbols('low_squared high_squared', positive=True)
    residue_low = sym.Matrix([[momentum_squared - low_squared, -2 * sym.I * chemical * low_energy], [2 * sym.I * chemical * low_energy, momentum_squared + radial_mass_squared - low_squared]]) / (2 * low_energy * separation)
    residue_high = sym.Matrix([[high_squared - momentum_squared, 2 * sym.I * chemical * high_energy], [-2 * sym.I * chemical * high_energy, high_squared - momentum_squared - radial_mass_squared]]) / (2 * high_energy * separation)
    for row in range(2):
        for column in range(2):
            commutator = (residue_low - residue_low.T + residue_high - residue_high.T)[row, column]
            verify(f'canonical_equal_time_field_{row}_{column}', commutator)
            moment = (low_energy * (residue_low + residue_low.T) + high_energy * (residue_high + residue_high.T))[row, column]
            verify(f'canonical_momentum_sum_{row}_{column}', moment.subs(separation, high_squared - low_squared), 1 if row == column else 0)
    first_radial, first_phase, first_mixing, second_radial, second_phase, second_mixing = sym.symbols('first_radial first_phase first_mixing second_radial second_phase second_mixing', real=True)
    first = sym.Matrix([[first_radial, sym.I * first_mixing], [-sym.I * first_mixing, first_phase]])
    second = sym.Matrix([[second_radial, sym.I * second_mixing], [-sym.I * second_mixing, second_phase]])
    verify('two_particle_weight_uses_transpose_not_adjoint', sym.trace(first * second.T), first_radial * second_radial + first_phase * second_phase - 2 * first_mixing * second_mixing)

    vertex_radial, vertex_phase = sym.symbols('vertex_radial vertex_phase', positive=True)
    external = sym.Matrix([sym.sqrt(vertex_radial), sym.I * sym.sqrt(vertex_phase)])
    phase_vertex = sym.Matrix([[0, cubic[(0, 1, 1)]], [cubic[(0, 1, 1)], 0]])
    radial_vertex = sym.diag(cubic[(0, 0, 0)], cubic[(0, 1, 1)])
    verify('elastic_phase_exchange_source_cancels', (external.conjugate().T * phase_vertex * external)[0])
    radial_source = (external.conjugate().T * radial_vertex * external)[0]
    verify('elastic_radial_exchange_source', radial_source, cubic[(0, 0, 0)] * vertex_radial + cubic[(0, 1, 1)] * vertex_phase)
    angle = sym.symbols('angle', real=True)
    legendre = (3 * angle**2 - 1) / 2
    verify('contact_and_total_momentum_s_channel_have_no_l2', sym.integrate(legendre, (angle, -1, 1)))
    inverse_argument = sym.symbols('inverse_argument', positive=True)
    verify('Q2_first_nonzero_large_argument_moment', sym.integrate(legendre * angle**2, (angle, -1, 1)) / 2, sym.Rational(2, 15))
    verify('Q2_leading_moment_zero', sym.integrate(legendre, (angle, -1, 1)) / 2)
    verify('Q2_next_moment_zero', sym.integrate(legendre * angle, (angle, -1, 1)) / 2)
    ratio, small_parameter = sym.symbols('ratio small_parameter', positive=True)
    mass_ratio = (2 * ratio - sym.Rational(2, 3)) / (1 + ratio)
    verify('preferred_branch_radial_mass_lower_bound_remainder', mass_ratio - sym.Rational(2, 3), 4 * (ratio - 1) / (3 * (ratio + 1)))
    born_bound = 2 * small_parameter * (6 * ratio - sym.Rational(2, 9))**2 / ((1 + ratio) * (2 * ratio - sym.Rational(2, 3)))
    verify('uniform_born_bound_positive_numerator', (36 * small_parameter - born_bound) * (1 + ratio) * (2 * ratio - sym.Rational(2, 3)) / small_parameter, (4320 * ratio - 1952) / 81)
    parent = PARENT / 'results/stage-integrity.json'
    report = {
        'state': 'complete', 'created_at': datetime.now(timezone.utc).isoformat(), 'checks': checks,
        'exact_checks': len(checks), 'potential': str(potential),
        'cubic_vertices': {''.join(map(str, key)): str(value) for key, value in cubic.items()},
        'quartic_vertices': {''.join(map(str, key)): str(value) for key, value in quartic_vertices.items()},
        'inverse_propagator': str(inverse), 'determinant': str(determinant),
        'spectral_pair_weight': 'tr(R_a(k) R_b(p)^T), not tr(R_a(k) R_b(p))',
        'elastic_com_l2_projection': 'A2(k) = J_sigma(k)^2/k^2 * Q2(1+M_a_squared/(2k^2)); A_l=(1/2)int_-1^1 P_l(z) M(z) dz; external LSZ weights Z_a=2 E_a R_a',
        'infrared_l2_behavior': '16 J_sigma(0)^2 k^4/(15 M_a_squared^3) + O(k^6)',
        'uniform_tree_projection_bound': '|A2| <= 36 epsilon with epsilon=mu^2/varrho0^2 on y>1; not a Bethe-Salpeter spectral-radius bound',
        'collective_pole_condition': 'An eigenvalue of the properly renormalized two-particle irreducible l=2 kernel times full two-line propagator must reach one, with nonzero stress overlap and healthy residue. No arbitrary separable coupling is introduced.',
        'interacting_pole_equation_solved': False,
        'parent_sha256': hashlib.sha256(parent.read_bytes()).hexdigest(),
        'scope': 'Full quadratic mixing, exact action-derived cubic/quartic vertices, and tree elastic COM quadrupolar projection. Gaussian continuum and tree projection are not a nonperturbative pole search.',
    }
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'cubic_entries': len(cubic), 'quartic_entries': len(quartic_vertices)}))


if __name__ == '__main__':
    main()
