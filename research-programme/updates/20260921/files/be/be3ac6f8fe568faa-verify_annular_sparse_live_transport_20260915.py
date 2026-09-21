from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_live_repaired_20260915 import SparseRepairedLiveSystem, SparseMaterial, SparseDensity
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState, DensityTable
from annular_repaired_live_current_20260915 import LiveTangent
from annular_sparse_live_tangent_20260915 import SparseLiveTangent
import numpy as np


def main():
    evidence = EvidenceRun('annular-sparse-live-transport-controls-attempt01', __file__)
    try:
        for gram in [False, True]:
            branch = 'MTS' if gram else 'reference'
            sparse = SparseRepairedLiveSystem(33, gram, 8, 10)
            dense = RepairedLiveSystem(33, gram, 8, 10)
            coordinates, momenta, rates, geometry = sparse.initial()
            labels = sparse.labels
            coordinates[:, :-1] *= 1+.05*labels[:, None]+.03*labels[:, None]**2
            coordinates[:, -1] += .0001*(1-4*labels**2)
            momenta[:, :-1] *= 1-.04*labels[:, None]+.02*labels[:, None]**3
            momenta[:, -1] += 2e-6*(1+labels)
            sparse_rates, sparse_geometry = sparse.solve(coordinates, momenta)
            dense_rates, dense_geometry = dense.solve(coordinates, momenta)
            sparse_force = sparse.forces(coordinates, sparse_rates, sparse_geometry)
            dense_force = dense.forces(coordinates, dense_rates, dense_geometry)
            row = dict(branch=branch, nonaffine_source_and_fields=True,
                rate_error=float(np.max(abs(sparse_rates-dense_rates))), force_error=float(np.max(abs(sparse_force-dense_force))),
                geometry_error=float(np.max(abs(sparse_geometry.mass_nodes-dense_geometry.mass_nodes))))
            evidence.check(branch+'_nonaffine_canonical_geometry_and_force', max(row[name] for name in ['rate_error', 'force_error', 'geometry_error']) < 2e-11, row)
            targets = np.unique(np.concatenate([np.linspace(5.19, 6.81, 101), coordinates[:, -1], sparse.base-.01, sparse.base+.01]))
            sparse_density = SparseDensity(SparseMaterial(sparse, coordinates), targets)
            dense_density = DensityTable(MaterialState(dense, coordinates), targets)
            sparse_density.update(sparse_rates)
            dense_density.update(sparse_rates)
            row['density_error'] = float(max(np.max(abs(getattr(sparse_density, name)-getattr(dense_density, name)))
                for name in ['temporal_square', 'gradient_square', 'gram', 'source_density', 'velocity']))
            totals = np.bincount(sparse_density.indices, weights=sparse_density.label_weights, minlength=len(targets))
            row['weight_normalization_error'] = float(np.max(abs(totals-1.)))
            row['minimum_label_weight'] = float(np.min(sparse_density.label_weights))
            evidence.check(branch+'_nonaffine_densities_and_positive_normalized_average', row['density_error'] < 2e-10
                and row['weight_normalization_error'] < 2e-13 and row['minimum_label_weight'] >= -1e-28, row)
            tangent = SparseLiveTangent(sparse, coordinates, momenta)
            layer_data = tangent.layer_data(.07)
            layer, position, velocity, acceleration = layer_data[:4]
            radius = layer_data[4]['radius']
            original = LiveTangent.regular_dual_dot(tangent, layer, position, velocity, acceleration, radius)
            optimized = tangent.regular_dual_dot(layer, position, velocity, acceleration, radius)
            row['transport_density_error'] = float(np.max(abs(original-optimized)))
            evidence.check(branch+'_sparse_transport_density_equivalence', row['transport_density_error'] < 2e-11, row)
            row['noether'] = tangent.noether(.07)
            evidence.check(branch+'_off_shell_Noether_including_moving_interface', row['noether']['noether'] < 2e-10, row)
            evidence.report['cases'].append(row)
            evidence.save()
            print(row, flush=True)
        evidence.report.update(nonaffine_source_control_not_new_physical_preparation=True,
            averaged_fields_not_replaced_by_single_middle_layer=True,
            full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
