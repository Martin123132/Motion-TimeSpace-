from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_characteristic_field_20260917 import FullCharacteristicField
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_flat_preassembled_flow_20260916 import FlatPreassembledFlow
from annular_characteristic_galerkin_defect_20260917 import nodal_reference
from annular_instantaneous_force_bridge_20260917 import reference_force_rate
from annular_smoothed_comparison_20260918 import source_curvature_jump
from derive_annular_characteristic_source_20260917 import rhs
import numpy as np


def main():
    evidence = EvidenceRun('annular-source-curvature-comparison-attempt01', __file__)
    try:
        evidence.report.update(original_action_unchanged=True, finite_future_trajectories_read=False,
            no_nonlinear_finite_trajectory_rerun=True, old_peak_force_gates_unchanged=True,
            projection_amplitude_not_used_as_fitted_input=True)
        reference = FullCharacteristicField(tight=True)
        for base_count in [129, 257, 513, 1025]:
            system = LocallyRefinedSourceAction(base_count, True, background_mass=0., source_splits=8)
            model = FlatPreassembledFlow(system)
            kink = np.maximum(system.radii-system.anchor, 0.)**2/2
            factor = model.lifted @ kink
            active = abs(factor) > 2e-12
            source_index = np.searchsorted(system.edges, system.anchor)
            left_element, right_element = source_index-1, source_index
            lengths = np.diff(system.edges)
            for instant in [.071, .195, .21, .4]:
                source = reference.source.sol(instant)
                position, speed = source[:2]
                acceleration = rhs(instant, source)[1]
                traces = reference_force_rate(instant, source, reference.initial)
                physical = (-2*speed*traces['trace_rates']-(acceleration+2/position)*traces['traces'])/(1-speed**2)
                jacobians = np.array([(position-5.2)/.83, (6.8-position)/.77])
                independent = jacobians[1]**2*physical[1]-jacobians[0]**2*physical[0]
                direct = source_curvature_jump(system, reference, instant)
                key = str(base_count)+'_'+str(instant)
                evidence.check(key+'_curvature_from_wave_and_moving_boundary', abs(independent-direct) < 2e-10,
                    float(abs(independent-direct)))
                state, unused = nodal_reference(system, reference, instant)
                nodal = np.where(system.element_indices >= 0, state[:system.count][system.element_indices], 0.)
                second = nodal @ np.array([4., -8., 4.])/lengths**2
                nodal_jump = second[right_element]-second[left_element]
                original_factor = model.lifted @ state[:system.count]
                projected = float(original_factor[active] @ factor[active]/(factor[active] @ factor[active]))
                evidence.report['cases'].append(dict(base_count=base_count, time=instant, h=system.gram_spacing,
                    exact_curvature_jump=float(direct), independent_curvature_jump=float(independent),
                    source_P2_second_jump=float(nodal_jump), local_factor_projection=projected,
                    source_P2_curvature_error=float(nodal_jump-direct)))
                evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
