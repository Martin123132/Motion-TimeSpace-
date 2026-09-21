from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState, material_weight
import numpy as np
import time


def main():
    evidence = EvidenceRun('annular-repaired-live-geometry-attempt01', __file__)
    try:
        points, weights = np.polynomial.legendre.leggauss(16)
        evidence.check('positive_continuous_material_weight_normalized',
                       abs(weights @ material_weight(points/2)/2-1) < 2e-14 and np.min(material_weight(points/2)) > 0)
        for gram in [False, True]:
            for degree in [4, 8]:
                started = time.perf_counter()
                system = RepairedLiveSystem(17, gram, degree, 10)
                coordinates, momenta, expected_rates, prepared = system.initial()
                rates, geometry = system.solve(coordinates, momenta)
                radial = geometry.off_grid_residual(rates)
                nodal = system.canonical_residual(coordinates, momenta, rates, geometry)
                off_grid = system.canonical_residual(coordinates, momenta, rates, geometry, True)
                row = dict(branch='MTS' if gram else 'reference', layer_degree=degree, scalar_count=17,
                           radial_degree=10, width=system.width, kappa=system.coupling,
                           canonical_roundtrip=float(np.max(abs(rates-expected_rates))), nodal_momentum_error=nodal,
                           off_grid_momentum_error=off_grid, mass_radial_residual=radial[0], lapse_radial_residual=radial[1],
                           exterior_mass=float(geometry.mass_nodes[-1, -1]), radial_iterations=geometry.radial_iterations,
                           canonical_iterations=geometry.canonical_iterations, seconds=time.perf_counter()-started)
                evidence.report['cases'].append(row)
                raw = evidence.output/(row['branch']+'-'+str(degree)+'.npz')
                np.savez_compressed(raw, coordinates=coordinates, momenta=momenta, rates=rates,
                                    radial_nodes=geometry.nodes, mass=geometry.mass_nodes, log_lapse=geometry.log_lapse_nodes)
                evidence.own(raw, 'outputs')
                prefix = row['branch']+str(degree)
                evidence.check(prefix+'_canonical_and_radial_fixed_points', nodal < 2e-10 and row['canonical_roundtrip'] < 2e-10, row)
                evidence.check(prefix+'_independent_off_grid_radial_equations', max(radial) < 2e-8, radial)
                evidence.check(prefix+'_nonzero_live_loading', row['exterior_mass'] > system.central_mass+1e-4)
                print(row, flush=True)
        for branch in ['reference', 'MTS']:
            rows = [row for row in evidence.report['cases'] if row['branch'] == branch]
            evidence.check(branch+'_material_interpolation_refines', rows[1]['off_grid_momentum_error'] < 2e-9
                           and rows[1]['off_grid_momentum_error'] <= max(rows[0]['off_grid_momentum_error']*.2, 2e-12), rows)
        evidence.report.update(repaired_action_live_radial_snapshot_solved=True,
                               continuous_finite_width_density_before_metric_products=True,
                               material_method='Chebyshev label collocation; not claimed as exact finite-label variational closure.',
                               live_evolution_completed=False, independent_temporal_current_tested=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
