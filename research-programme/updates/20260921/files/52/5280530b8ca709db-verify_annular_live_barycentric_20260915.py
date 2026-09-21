from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-live-barycentric-equivalence-attempt01', __file__)
    try:
        for degree in [64, 192, 384]:
            if degree == 384:
                path = evidence.output.parent/'annular-live-continuum-refinement-attempt02/degree384.npz'
                parameters = dict(degree=384, layer_degree=8, radial_degree=18, radial_spacing=.025, label_order=12)
            else:
                path = evidence.output.parent/'annular-live-continuum-evolution-attempt01'/('degree'+str(degree)+'-main.npz')
                parameters = dict(degree=degree, layer_degree=4, radial_degree=14, radial_spacing=.05, label_order=8)
            evidence.own(path)
            saved = np.load(path)
            dense, factored = LiveContinuumCharacteristics(**parameters), BarycentricLiveContinuum(**parameters)
            for index in [0, -1]:
                started = time.perf_counter()
                original_flow, original_geometry, unused = dense.rhs_with_geometry(saved['states'][index])
                dense_seconds = time.perf_counter()-started
                started = time.perf_counter()
                fast_flow, fast_geometry, unused = factored.rhs_with_geometry(saved['states'][index])
                fast_seconds = time.perf_counter()-started
                row = dict(degree=degree, index=index, dense_seconds=dense_seconds, barycentric_seconds=fast_seconds,
                           flow_error=float(np.max(abs(original_flow-fast_flow))),
                           geometry_error=float(max(np.max(abs(original_geometry.mass_nodes-fast_geometry.mass_nodes)),
                                                    np.max(abs(original_geometry.log_lapse_nodes-fast_geometry.log_lapse_nodes)))),
                           density_error=float(np.max(abs(original_geometry.density.square-fast_geometry.density.square))))
                evidence.report['cases'].append(row)
                print(row, flush=True)
                evidence.check(str(degree)+'_'+str(index)+'_same_interpolant_geometry_and_flow', row['flow_error'] < 2e-11
                               and row['geometry_error'] < 2e-13 and row['density_error'] < 2e-13, row)
        evidence.report.update(full_polynomial_interpolant_retained=True, no_degree_truncation_or_boundary_fit=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
