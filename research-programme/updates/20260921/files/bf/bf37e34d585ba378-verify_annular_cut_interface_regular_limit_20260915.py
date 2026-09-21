from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction
import sympy as sp
import numpy as np


def main():
    evidence = EvidenceRun('annular-cut-interface-regular-limit-attempt01', __file__)
    try:
        spacing, fraction, mismatch = sp.symbols('h theta q_b', positive=True)
        energy = mismatch**2/(2*spacing*fraction)+mismatch**2/(2*spacing*(1-fraction))
        evidence.check('nonzero_initial_trace_injects_inverse_mesh_energy',
                       sp.simplify(energy-mismatch**2/(2*spacing*fraction*(1-fraction))) == 0)
        for count in [17, 33, 65, 129, 257]:
            system = CurvedCutAction(count, True)
            for phase in [.2, .5, .8]:
                position = system.radii[count//2]+phase*system.spacing
                offset = system.radii-position
                scalar = np.where(offset < 0, .02*offset+.015*offset**2, -.015*offset-.02*offset**2)
                coefficient = system.sampling @ system.coefficient(0., system.radii)
                factors = system.lifted(position) @ scalar
                energy = np.dot(coefficient, factors**2)/(2*system.spacing)
                shifted = system.lifted(position+1e-24j) @ scalar
                force = -np.dot(coefficient, shifted**2).imag/(2*system.spacing*1e-24)
                evidence.check(str(count)+str(phase)+'_finite_positive_full_factor_energy', energy > 0 and np.isfinite(force))
                evidence.report['cases'].append(dict(count=count, phase=phase, spacing=system.spacing,
                    energy=float(energy), force=float(force), energy_over_h_cubed=float(energy/system.spacing**3),
                    absolute_force_over_h=float(abs(force)/system.spacing)))
        worst = []
        for count in [17, 33, 65, 129, 257]:
            rows = [row for row in evidence.report['cases'] if row['count'] == count]
            worst.append(dict(count=count, spacing=rows[0]['spacing'], energy=max(row['energy'] for row in rows),
                              force=max(abs(row['force']) for row in rows)))
        energy_order = np.log(worst[-2]['energy']/worst[-1]['energy'])/np.log(2)
        force_order = np.log(worst[-2]['force']/worst[-1]['force'])/np.log(2)
        evidence.check('second_derivative_jump_energy_has_third_order_decay', energy_order > 2.8, float(energy_order))
        evidence.check('full_shape_force_has_at_least_first_order_decay', force_order > .8, float(force_order))
        evidence.report.update(scope='Piecewise quadratic zero-trace histories with unequal one-sided curvatures; not a dynamic stability proof.',
                               energy_order=float(energy_order), force_order=float(force_order), worst_by_count=worst,
                               conditional_bound='For fixed phase margin eta>0, bounded one-sided C2 norms and uniformly bounded finite-stencil weights: E_interface=O(h^3), partial_b E_interface=O(h).',
                               source_phase_margin=.2,
                               uniform_near_cell_crossing_bound_proven=False,
                               all_Gram_rows_and_weights_retained=True,
                               pointwise_second_derivative_jump_resolved_exactly=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
