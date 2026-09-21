from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System, indexed_label_values
from annular_P2_graded_source_20260919 import GradedP2System
from annular_live_P2_current_20260918 import LiveP2Tangent
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-indexed-live-geometry-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, new_evolution_performed=False,
            optimization_only=True, modes_and_quadrature_unchanged=True,
            canonical_and_radial_tolerances_unchanged=True, maximum_wall_seconds=1800.)
        rng = np.random.default_rng(20919)
        for complex_case in [False, True]:
            interpolation = rng.normal(size=(137, 15))
            values = rng.normal(size=(15, 554))
            if complex_case:
                values = values+1j*rng.normal(size=values.shape)
            indices = rng.integers(0, 554, size=(137, 3))
            expected = (interpolation @ values)[np.arange(137)[:, None], indices]
            actual = indexed_label_values(interpolation, values, indices)
            error = float(np.max(abs(actual-expected)))
            evidence.check('indexed_dense_algebra_'+str(complex_case), error < 5e-14, error)
        for branch in ['reference', 'MTS']:
            folder = 'annular-P2-live-exponential-'+branch+'-257-attempt01'
            saved = checked_load(evidence, folder, 'trajectory-steps16.npz')
            status_path = evidence.output.parent/folder/'status.json'
            status = json.loads(status_path.read_text())
            evidence.own(status_path)
            original = GradedP2System(257, branch == 'MTS', 4e-5)
            indexed = IndexedGradedP2System(257, branch == 'MTS', 4e-5)
            for tag, state in [('initial', saved['states'][0]), ('evolved', saved['states'][-1])]:
                if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                    raise RuntimeError('Indexed comparison safe wall budget reached.')
                coordinates, momenta = state
                measured = perf_counter()
                old_rates, old_geometry = original.solve(coordinates, momenta)
                old_forces = original.forces(coordinates, old_rates, old_geometry)
                old_seconds = perf_counter()-measured
                measured = perf_counter()
                rates, geometry = indexed.solve(coordinates, momenta)
                forces = indexed.forces(coordinates, rates, geometry)
                new_seconds = perf_counter()-measured
                old_density, density = old_geometry.density, geometry.density
                prefix = branch+'_'+tag+'_'
                evidence.check(prefix+'identical_geometry_mesh', np.array_equal(geometry.nodes, old_geometry.nodes))
                evidence.check(prefix+'same_label_quadrature_shape', density.offsets.shape == old_density.offsets.shape
                    and np.array_equal(density.indices, old_density.indices))
                label_error = float(np.max(abs(density.offsets-old_density.offsets)))
                weight_error = float(np.max(abs(density.label_weights-old_density.label_weights)))
                evidence.check(prefix+'same_label_quadrature_values', label_error < 3e-14 and weight_error < 3e-14,
                    dict(labels=label_error, weights=weight_error))
                density_error = {name:float(np.max(abs(getattr(density, name)-getattr(old_density, name))))
                    for name in ['gradient_square', 'temporal_square', 'gram', 'source_density', 'velocity']}
                evidence.check(prefix+'all_density_terms_retained', max(density_error.values()) < 2e-12, density_error)
                rate_error = float(np.max(abs(rates-old_rates)))
                force_error = float(np.max(abs(forces-old_forces)))
                source_force_error = float(np.max(abs(forces[:, -1]-old_forces[:, -1])))
                evidence.check(prefix+'full_live_RHS_matches', rate_error < 2e-11 and force_error < 2e-9
                    and source_force_error < 2e-11, dict(rate_error=rate_error, covector_error=force_error,
                        source_covector_error=source_force_error))
                metric_error = max(float(np.max(abs(geometry.mass_nodes-old_geometry.mass_nodes))),
                    float(np.max(abs(geometry.log_lapse_nodes-old_geometry.log_lapse_nodes))))
                evidence.check(prefix+'constrained_metric_matches', metric_error < 2e-12, metric_error)
                canonical = indexed.canonical_residual(coordinates, momenta, rates, geometry)
                radial = geometry.off_grid_residual(rates)
                evidence.check(prefix+'canonical_and_offgrid_radial_constraints', canonical < 2e-11
                    and max(radial) < 2e-9, dict(canonical=canonical, radial=radial))
                samples = len(density.offsets)
                row = dict(branch=branch, state=tag, old_RHS_seconds=old_seconds, indexed_RHS_seconds=new_seconds,
                    observed_RHS_speed_ratio=old_seconds/new_seconds, label_samples=samples,
                    label_difference=label_error, weight_difference=weight_error, density_differences=density_error,
                    rate_difference=rate_error, covector_difference=force_error, source_covector_difference=source_force_error,
                    metric_difference=metric_error, canonical=canonical, radial=list(radial),
                    old_dense_sample_temporary_bytes=samples*(indexed.count+1)*8,
                    indexed_gather_plus_local_output_bytes=samples*(len(indexed.labels)+3)*8,
                    memory_formula_not_process_peak_measurement=True)
                evidence.report['cases'].append(row)
                evidence.save()
                print(json.dumps(dict(branch=branch, state=tag, speed_ratio=row['observed_RHS_speed_ratio'],
                    old_seconds=old_seconds, new_seconds=new_seconds, rate_error=rate_error,
                    covector_error=force_error)), flush=True)
                del old_geometry, old_density, geometry, density
            tangent = LiveP2Tangent(indexed, *saved['states'][-1])
            current = tangent.layer_data(0.)
            actual, expected = -current.wave_source_euler, status['cases'][-1]['reduced_wave_force']
            force_change = float(abs(actual-expected))
            evidence.check(branch+'_true_reduced_force_unchanged', force_change < 2e-10,
                dict(indexed=float(actual), original=expected, difference=force_change))
            noether = current.noether()
            evidence.check(branch+'_moving_current_and_Euler_unchanged', noether['residual'] < 2e-9
                and noether['source_euler'] < 2e-8 and noether['scalar_euler'] < 2e-8, noether)
            evidence.report.setdefault('force_controls', []).append(dict(branch=branch, force=float(actual),
                original_force=expected, difference=force_change, noether=noether))
            evidence.save()
        evidence.report.update(seconds=perf_counter()-started,
            qualified_at_saved_initial_and_evolved_states_only=True,
            full_window_speedup_not_measured=True, scientific_trajectory_results_unchanged=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']),
            seconds=perf_counter()-started, force_controls=evidence.report['force_controls'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
