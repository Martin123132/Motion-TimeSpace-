from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction, scalar_pencil
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_bulk_refinement_20260919 import indexed_initial, gram_jump_split
from scipy.linalg import solve_banded, eigvalsh
import contextlib
import json
import numpy as np
import sympy as symbolic


def main():
    evidence = EvidenceRun('annular-P2-Gram-jump-scale-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_forward_evolution=True,
            isolated_dyad_not_full_coercivity=True, bubble_trial_gives_scalar_spectral_lower_bound=True,
            no_uniform_nonlinear_stability_claim=True, no_terms_removed=True)
        phase = symbolic.symbols('phase', real=True)
        hinge_difference = symbolic.Matrix([1-phase, 2*phase-1, -phase])
        gram = symbolic.Matrix([[10, -1, 0], [-1, 10, -1], [0, -1, 10]])/144
        coefficient = symbolic.expand((hinge_difference.T*gram*hinge_difference)[0])
        expected = (34*phase**2-34*phase+11)/72
        evidence.check('exact_interior_phase_polynomial', symbolic.simplify(coefficient-expected) == 0)
        evidence.check('exact_phase_minimum_and_maximum', coefficient.subs(phase, symbolic.Rational(1, 2)) == symbolic.Rational(5, 144)
            and coefficient.subs(phase, 0) == symbolic.Rational(11, 72)
            and symbolic.diff(coefficient, phase, 2) > 0)
        mass = symbolic.Matrix([[4, 2], [2, 16]])/30
        derivative = symbolic.Matrix([1, -4])
        evidence.check('source_zero_P2_trace_dual_norm', (derivative.T*mass.inv()*derivative)[0] == 48)
        evidence.check('source_midpoint_bubble_trace_norm', derivative[1]**2/mass[1, 1] == 30)
        evidence.check('constant_phase_negative_control', coefficient.subs(phase, symbolic.Rational(1, 5))
            != coefficient.subs(phase, symbolic.Rational(2, 5)))
        fixtures = []
        for count in [65, 129, 257, 513]:
            for cap in [4e-5, 2e-5, 1e-5]:
                layer = GradedSourceAction(count, True, source_cap=cap)
                spacing = layer.gram_spacing
                coordinate = (layer.anchor-layer.base_radii[0])/spacing
                fraction = coordinate-np.floor(coordinate)
                predicted = spacing*(34*fraction**2-34*fraction+11)/72
                actual = float(layer.lifted_hinge @ layer.lifted_hinge/spacing)
                source = int(np.searchsorted(layer.edges, layer.anchor))
                lengths = np.diff(layer.edges)[source-1:source+1]
                bands = np.zeros((5, layer.count))
                local_mass = np.array([[4., 2., -1.], [2., 16., 2.], [-1., 2., 4.]])/30
                for indices, length in zip(layer.element_indices, np.diff(layer.edges)):
                    for first in range(3):
                        for second in range(3):
                            row, column = indices[first], indices[second]
                            if row >= 0 and column >= 0:
                                bands[2+row-column, column] += length*local_mass[first, second]
                dual = float(layer.jump @ solve_banded((2, 2), bands, layer.jump, check_finite=False))
                lower, upper = 30*np.sum(lengths**-3), 48*np.sum(lengths**-3)
                key = str(count)+'_'+str(cap)
                evidence.check(key+'_hinge_phase_coefficient', abs(actual-predicted) < 2e-12*max(1., abs(predicted)))
                evidence.check(key+'_jump_dual_bracket', lower*(1-1e-12) <= dual <= upper*(1+1e-12))
                bubble_indices = layer.element_indices[[source-1, source], 1]
                evidence.check(key+'_bubble_is_in_original_Gram_kernel',
                    np.max(abs(layer.original[:, bubble_indices].toarray()), initial=0.) == 0)
                fixtures.append(dict(base_count=count, source_cap=cap, phase=float(fraction),
                    coefficient=actual, predicted=predicted, jump_dual_norm=dual,
                    lower=lower, upper=upper, source_lengths=lengths.tolist()))
        physical = []
        for count, cap in [(257, 2e-5), (513, 1e-5)]:
            system = IndexedGradedP2System(count, True, cap)
            coordinates, unused, unused2, geometry = indexed_initial(system)
            layer = system.layer(0., geometry)
            values = coordinates[len(system.labels)//2]
            mass, stiffness = scalar_pencil(layer, values)
            split = gram_jump_split(layer, values, mass)
            source = int(np.searchsorted(layer.edges, layer.anchor))
            indices = layer.element_indices[[source-1, source], 1]
            local = mass[np.ix_(indices, indices)]
            vector = np.zeros(layer.count)
            vector[indices] = np.linalg.solve(local, layer.jump[indices])
            norm_squared = float(layer.jump @ vector)
            lower = split['jump_penalty_coefficient']*norm_squared
            rayleigh = float(vector @ stiffness @ vector/(vector @ mass @ vector))
            maximum = float(eigvalsh(stiffness, mass, subset_by_index=[layer.count-1, layer.count-1], check_finite=False)[0])
            evidence.check(str(count)+'_full_scalar_bubble_spectral_bracket',
                np.max(abs(layer.original @ vector), initial=0.) == 0
                and lower <= rayleigh*(1+2e-10) and rayleigh <= maximum*(1+2e-10))
            physical.append(dict(base_count=count, source_cap=cap, gram_split=split,
                bubble_lower_frequency=float(np.sqrt(lower)),
                bubble_Rayleigh_frequency=float(np.sqrt(rayleigh)), full_scalar_maximum_frequency=float(np.sqrt(maximum))))
        evidence.report.update(cases=fixtures, physical_initial_controls=physical,
            phase_formula='(34 theta^2-34 theta+11)/72',
            conditional_jump_dual_lower='30 sum_side[1/(Kmax_side delta_side^3)]',
            conditional_jump_dual_upper='48 sum_side[1/(Kmin_side delta_side^3)]')
        for name in ['status.json', 'coefficients.json', 'COMPLETE']:
            evidence.own(evidence.root/'source-intake/navier-stokes/20260909/sbp4-second-derivative-derived'/name)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), physical=physical)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
