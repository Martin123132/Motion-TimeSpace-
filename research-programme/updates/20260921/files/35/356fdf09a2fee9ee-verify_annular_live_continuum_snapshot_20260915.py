from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-live-continuum-snapshot-attempt01', __file__)
    try:
        for degree in [32, 64, 96]:
            started = time.perf_counter()
            system = LiveContinuumCharacteristics(degree=degree)
            state, geometry = system.initial()
            flow, geometry, forces = system.rhs_with_geometry(state)
            radial = geometry.check_radial()
            current = system.current_test(state)
            raw = evidence.output/('degree'+str(degree)+'.npz')
            np.savez_compressed(raw, state=state, flow=flow, radial_nodes=geometry.nodes, mass=geometry.mass_nodes,
                                log_lapse=geometry.log_lapse_nodes, **current)
            evidence.own(raw, 'outputs')
            row = dict(degree=degree, layer_degree=4, radial_degree=10, width=.02, coupling=.1,
                       mass_radial=radial[0], lapse_radial=radial[1], current_error=current['error'],
                       velocity_preparation_error=float(np.max(abs(forces['velocity']-.03))),
                       minimum_material_jacobian=geometry.material.minimum_jacobian,
                       mass_exterior=float(geometry.mass_nodes[-1, -1]),
                       force_middle=float(forces['radiation'][2]), seconds=time.perf_counter()-started)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
            evidence.check(str(degree)+'_finite_ordered_live_initial_solve', np.all(np.isfinite(flow)) and row['minimum_material_jacobian'] > 0, row)
            evidence.check(str(degree)+'_same_velocity_preparation', row['velocity_preparation_error'] < 2e-10, row)
            evidence.check(str(degree)+'_independent_radial_constraints', max(radial) < 2e-7, row)
        evidence.report.update(independent_live_continuum_snapshot_constructed=True, temporal_current_accuracy_not_yet_qualified=True,
                               current_diagnostic_not_an_acceptance_pass=True, same_original_repaired_live_preparation=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
