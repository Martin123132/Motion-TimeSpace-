from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_midpoint_20260921 import LiveCommonEvaluation, midpoint_step
from derive_annular_candidate_midpoint_20260921 import saved_matrix, save_step, difference
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_decimal_transport_v2_20260919 import decimal_array
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal
from time import perf_counter
import contextlib
import json
import numpy as np


def decimals(values):
    return np.array([[Decimal(value) for value in row] for row in values])


def main():
    evidence = EvidenceRun('annular-candidate-midpoint-quadrature-attempt01', __file__)
    started = perf_counter()
    deadline = started+2400
    try:
        path = evidence.output.parent/'annular-candidate-coupled-midpoint-attempt01/status.json'
        source = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('completed_main_trajectory_source', source['state'] == 'complete'
            and all(row['passed'] for row in source['checks']) and source['new_coupled_evolution'])
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
            original_live_action_unchanged=True, modes_deleted=False, new_coupled_evolution=False,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            spatial_convergence_proven=False, general_nonzero_shift_or_temporal_current_derived=False,
            exact_finite_label_Galerkin_evolution_qualified=False, global_stability_proven=False,
            independent_quadrature_qualified=False, independent_reverse_qualified=False,
            perturbed_reversals=[], initial_physical_fields_and_velocities_preserved=True,
            comparison_uses_momentum_impulses_not_unequal_initial_quadrature_momenta=True,
            reference_order=16, material_order=48, radial_degree=22, radial_label_order=28,
            horizon=1e-7, horizon_has_no_seconds_assignment=True, iterations=[], comparisons=[])
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, unused, unused_rates = common_material(native, saved, packet)
            action = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
            initial = checked_load(evidence, 'annular-candidate-coupled-midpoint-attempt01', case+'-initial.npz')
            coarse = checked_load(evidence, 'annular-candidate-coupled-midpoint-attempt01', case+'-forward1-step1.npz')
            coordinates, rates = decimals(initial['coordinates']), initial['midpoint_rates']
            evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline,
                reference_order=16, material_order=48)
            preconditioner = BandedSourceInverse(saved_matrix(evidence, case+'-22-fixed-metric-mass.npz'), rates.shape)
            base = evaluator.evaluate(coordinates, rates)
            momenta = decimal_array(base['momentum'])
            save_step(evidence, case+'-initial', coordinates, momenta, rates, base, [])
            test_label = 'finer_quadrature'
            def record(row, midpoint, trial_rates, current, residual):
                evidence.report['iterations'].append(dict(branch=branch, extension=extension, label=test_label, **row, valid_for_claim=False))
                evidence.report['progress'] = dict(case=case, label=test_label, iteration=row['iteration'],
                    relative_residual=row['relative_residual'], maximum_correction=row['maximum_correction'],
                    seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
                np.savez_compressed(evidence.output/'latest-trial-recovery.npz', midpoint=np.array(midpoint, dtype=str),
                    rates=trial_rates, residual=residual, force=current['force'], metric=current['solution']['state'])
            position, momentum, velocity, current, history = midpoint_step(evaluator, coordinates, momenta,
                rates.copy(), 1e-7, preconditioner, record)
            save_step(evidence, case+'-fine-step', position, momentum, velocity, current, history)
            final = history[-1]
            evidence.check(case+'_same_strict_nonlinear_and_chart_gates', final['relative_residual'] < 5e-12
                and final['maximum_correction'] < 2e-12 and final['radial_residual'] < 2e-12
                and final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
            evidence.report['cases'].append(dict(branch=branch, extension=extension, label=test_label, digits=64, step=1e-7,
                full_components=16425, iterations=len(history), **{name:final[name] for name in
                    ['relative_residual', 'maximum_correction', 'radial_residual', 'minimum_F', 'maximum_speed_ratio']}, valid_for_claim=False))
            for component, fine_endpoint, fine_initial, coarse_name in [(0, position, coordinates, 'coordinates'),
                    (1, momentum, momenta, 'momenta')]:
                coarse_endpoint, coarse_initial = decimals(coarse[coarse_name]), decimals(initial[coarse_name])
                fine_increment = difference(fine_endpoint, fine_initial)
                coarse_increment = difference(coarse_endpoint, coarse_initial)
                for block, section in [('field', slice(None, -1)), ('source', slice(-1, None))]:
                    error = float(np.max(abs(fine_increment[:, section]-coarse_increment[:, section])))
                    signal = float(np.max(abs(coarse_increment[:, section])))
                    scale = max(float(np.max(abs(np.asarray(coarse_initial[:, section], float)))), 1e-30)
                    floor = (2e-15 if component == 0 else 5e-12)*scale
                    tolerance = 2e-3*signal+floor
                    evidence.report['comparisons'].append(dict(branch=branch, extension=extension, component=component,
                        block=block, increment_difference=error, motion_signal=signal, signal_relative_difference=error/max(signal, 1e-90),
                        roundoff_floor=floor, tolerance=tolerance, passed=error < tolerance, valid_for_claim=False))
            test_label = 'perturbed_reverse'
            reverse_evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline)
            rng = np.random.default_rng(20260921)
            seed = rates+3e-5*rng.standard_normal(rates.shape)
            seed[:, -1] = rates[:, -1]+2e-4*rng.standard_normal(len(rates))
            evidence.check(case+'_all_reverse_seed_components_perturbed', np.count_nonzero(seed-coarse['midpoint_rates']) == rates.size)
            seed_path = evidence.output/(case+'-perturbed-reverse-seed.npz')
            np.savez_compressed(seed_path, seed=seed, forward_midpoint_rates=coarse['midpoint_rates'], initial_rates=rates)
            evidence.own(seed_path, 'outputs')
            reverse = midpoint_step(reverse_evaluator, decimals(coarse['coordinates']), decimals(coarse['momenta']),
                seed, -1e-7, preconditioner, record)
            save_step(evidence, case+'-perturbed-reverse', *reverse)
            final = reverse[-1][-1]
            evidence.check(case+'_perturbed_reverse_nonlinear_and_chart_gates', final['relative_residual'] < 5e-12
                and final['maximum_correction'] < 2e-12 and final['radial_residual'] < 2e-12
                and final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
            evidence.report['cases'].append(dict(branch=branch, extension=extension, label=test_label, digits=64, step=-1e-7,
                full_components=16425, iterations=len(reverse[-1]), **{name:final[name] for name in
                    ['relative_residual', 'maximum_correction', 'radial_residual', 'minimum_F', 'maximum_speed_ratio']}, valid_for_claim=False))
            for component, name in [(0, 'coordinates'), (1, 'momenta')]:
                original = decimals(initial[name])
                for block, section in [('field', slice(None, -1)), ('source', slice(-1, None))]:
                    error = float(np.max(abs(difference(reverse[component][:, section], original[:, section]))))
                    scale = max(float(np.max(abs(np.asarray(original[:, section], float)))), 1e-30)
                    tolerance = (2e-14 if component == 0 else 2e-10)*scale
                    evidence.report['perturbed_reversals'].append(dict(branch=branch, extension=extension,
                        component=component, block=block, maximum_error=error, tolerance=tolerance,
                        passed=error < tolerance, all_16425_seed_components_perturbed=True, valid_for_claim=False))
            evidence.save()
        evidence.own(evidence.output/'latest-trial-recovery.npz', 'outputs')
        evidence.report.update(new_coupled_evolution=True,
            independent_quadrature_qualified=all(row['passed'] for row in evidence.report['comparisons']),
            independent_reverse_qualified=all(row['passed'] for row in evidence.report['perturbed_reversals']),
            seconds=perf_counter()-started)
        evidence.check('all_three_finer_quadrature_and_perturbed_reverse_cases', len(evidence.report['cases']) == 6
            and len(evidence.report['comparisons']) == 12 and len(evidence.report['perturbed_reversals']) == 12)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', qualified=evidence.report['independent_quadrature_qualified'],
            checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        recovery = evidence.output/'latest-trial-recovery.npz'
        if recovery.exists():
            evidence.own(recovery, 'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
