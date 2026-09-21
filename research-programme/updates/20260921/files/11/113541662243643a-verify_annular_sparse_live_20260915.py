from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_sparse_live_repaired_20260915 import SparseRepairedLiveSystem, SparseMaterial, SparseDensity
from annular_repaired_live_geometry_20260915 import RepairedLiveSystem, MaterialState, DensityTable
from annular_repaired_live_current_20260915 import LiveTangent
import numpy as np
import time


def maximum_error(first, second):
    return float(np.max(abs(np.asarray(first)-np.asarray(second))))


def main():
    evidence = EvidenceRun('annular-sparse-live-equivalence-attempt01', __file__)
    try:
        for count in [17, 33, 65]:
            for gram in [False, True]:
                branch = 'MTS' if gram else 'reference'
                dense = RepairedLiveSystem(count, gram, 8, 10)
                sparse = SparseRepairedLiveSystem(count, gram, 8, 10)
                evidence.check(f'{branch}-{count}_all_original_Gram_factors_retained',
                               maximum_error(dense.original, sparse.original.toarray()) < 1e-14 if gram else sparse.original.shape[0] == 0)
                path = evidence.output.parent/'annular-repaired-live-evolution-attempt01'/f'{branch}-{count}-main.npz'
                evidence.own(path)
                saved = np.load(path)
                for index in [0, -1]:
                    coordinates, momenta = saved['state'][:2*9*(count+1), index].reshape(2, 9, count+1)
                    started = time.perf_counter()
                    dense_rates, dense_geometry = dense.solve(coordinates, momenta)
                    dense_force = dense.forces(coordinates, dense_rates, dense_geometry)
                    dense_seconds = time.perf_counter()-started
                    started = time.perf_counter()
                    sparse_rates, sparse_geometry = sparse.solve(coordinates, momenta)
                    sparse_force = sparse.forces(coordinates, sparse_rates, sparse_geometry)
                    sparse_seconds = time.perf_counter()-started
                    row = dict(branch=branch, count=count, time=float(saved['time'][index]),
                               rate_error=maximum_error(dense_rates, sparse_rates), force_error=maximum_error(dense_force, sparse_force),
                               mass_error=maximum_error(dense_geometry.mass_nodes, sparse_geometry.mass_nodes),
                               lapse_error=maximum_error(dense_geometry.log_lapse_nodes, sparse_geometry.log_lapse_nodes),
                               dense_seconds=dense_seconds, sparse_seconds=sparse_seconds)
                    density = sparse_geometry.density
                    row['sparse_sample_shape_bytes'] = int(density.shape.nbytes)
                    row['dense_sample_shape_bytes'] = int(dense_geometry.density.shape.nbytes)
                    key = f'{branch}-{count}-{index}'
                    evidence.check(key+'_canonical_radial_force_equivalence', max(row[name] for name in ['rate_error', 'force_error', 'mass_error', 'lapse_error']) < 2e-11, row)
                    layer = sparse.layer(0., dense_geometry)
                    dense_layer = dense.layer(0., dense_geometry)
                    position, rate = coordinates[4], dense_rates[4]
                    left, right = dense_layer.evaluate(0., position, rate), layer.evaluate(0., position, rate)
                    names = ['action', 'wave_action', 'momenta', 'field_momenta', 'scalar_covector', 'nodal_dual']
                    row['action_components_error'] = max(maximum_error(left[name], right[name]) for name in names)
                    step = 1e-24
                    left = dense_layer.evaluate(0., position.astype(complex)+1j*step*rate, rate)
                    right = layer.evaluate(0., position.astype(complex)+1j*step*rate, rate)
                    row['directional_components_error'] = max(maximum_error(np.asarray(left[name]).imag/step, np.asarray(right[name]).imag/step) for name in names)
                    evidence.check(key+'_action_and_complex_transport_equivalence', max(row['action_components_error'], row['directional_components_error']) < 2e-10, row)
                    targets = np.unique(np.concatenate([np.linspace(5.19, 6.81, 61), np.linspace(6.015, 6.045, 31)]))
                    dense_density = DensityTable(MaterialState(dense, coordinates), targets)
                    sparse_density = SparseDensity(SparseMaterial(sparse, coordinates), targets)
                    dense_density.update(dense_rates)
                    sparse_density.update(dense_rates)
                    row['independent_density_error'] = max(maximum_error(getattr(dense_density, name), getattr(sparse_density, name))
                        for name in ['temporal_square', 'gradient_square', 'gram', 'source_density', 'velocity'])
                    evidence.check(key+'_averaged_density_all_components', row['independent_density_error'] < 2e-10, row)
                    if count == 17 and index == -1:
                        dense_tangent = LiveTangent(dense, coordinates, momenta)
                        sparse_tangent = LiveTangent(sparse, coordinates, momenta)
                        row['physical_radiation_force_error'] = float(abs(dense_tangent.layer_data(0.)[7]-sparse_tangent.layer_data(0.)[7]))
                        evidence.check(key+'_physical_force_retains_source_momentum_derivative', row['physical_radiation_force_error'] < 2e-10, row)
                    evidence.report['cases'].append(row)
                    evidence.save()
                    print(row, flush=True)
        evidence.report.update(same_equations_and_quadrature=True, all_Gram_rows_retained=True,
                               performance_measurement_not_accuracy_evidence=True,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
