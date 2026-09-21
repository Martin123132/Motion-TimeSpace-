from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from annular_two_sided_GR_characteristics_20260915 import TwoSidedGRCharacteristics
import numpy as np


def main():
    evidence = EvidenceRun('annular-characteristic-product-defect-attempt01', __file__)
    try:
        for degree in [64, 192]:
            live = LiveContinuumCharacteristics(degree, 4, 14, radial_spacing=.05, coupling=0.)
            unused, geometry = live.initial()
            source = geometry.material.source[0]
            static = TwoSidedGRCharacteristics(degree)
            static.inner -= .01
            static.outer -= .01
            radius, lengths, mesh_speed = static.mesh(source[0], .03)
            speed, speed_radial = 1-1.4/radius, 1.4/radius**2
            scaled = geometry.fields[0]
            physical = speed[:, None, :]*scaled
            initial = static.pack(physical, source)
            independent_flow = static.rhs(0., initial)
            plus, minus = scaled[:, 0], scaled[:, 1]
            plus_gradient = (plus @ static.derivative.T)/lengths[:, None]
            minus_gradient = (minus @ static.derivative.T)/lengths[:, None]
            curvature = speed/radius*(plus-minus)
            scaled_plus_flow = (speed+mesh_speed)*plus_gradient+speed_radial*plus+curvature
            scaled_minus_flow = (mesh_speed-speed)*minus_gradient-speed_radial*minus+curvature
            transformed_plus = speed*scaled_plus_flow+mesh_speed*speed_radial*plus
            transformed_minus = speed*scaled_minus_flow+mesh_speed*speed_radial*minus
            commutator_plus = ((speed*plus) @ static.derivative.T)/lengths[:, None]-speed*plus_gradient-speed_radial*plus
            commutator_minus = ((speed*minus) @ static.derivative.T)/lengths[:, None]-speed*minus_gradient-speed_radial*minus
            defect = np.stack([(speed+mesh_speed)*commutator_plus, (mesh_speed-speed)*commutator_minus], axis=1)
            transformed = static.pack(np.stack([transformed_plus, transformed_minus], axis=1), independent_flow[-3:])
            predicted = static.pack(defect, np.zeros(3))
            error = float(np.max(abs(independent_flow-transformed-predicted)))
            magnitude = float(np.max(abs(predicted)))
            row = dict(degree=degree, exact_semidiscrete_identity_error=error, product_rule_defect=magnitude)
            evidence.report['cases'].append(row)
            print(row, flush=True)
            evidence.check(str(degree)+'_finite_product_rule_defect_accounts_for_variable_change', error < 2e-11 and magnitude > 1e-10, row)
        rows = evidence.report['cases']
        evidence.check('product_defect_reduces_without_equation_change', rows[-1]['product_rule_defect'] < rows[0]['product_rule_defect'], rows)
        evidence.report.update(continuum_change_of_variables_exact=True, finite_collocation_product_rule_not_exact=True,
                               no_force_fit_or_continuum_equation_repair=True, full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
