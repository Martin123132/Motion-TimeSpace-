from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_midpoint_20260921 import LiveCommonEvaluation, midpoint_step
from annular_candidate_canonical_response_20260920 import common_material
from annular_candidate_coordinate_covectors_20260921 import scaled_error
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from scipy.sparse import load_npz
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import hashlib
import json
import numpy as np


def saved_matrix(evidence, filename):
    status_path = evidence.output.parent/'annular-candidate-full-canonical-inverse-attempt01/status.json'
    status = json.loads(status_path.read_text())
    path = status_path.parent/filename
    evidence.check(filename+'_owned_full_mass', status['state'] == 'complete' and
        hashlib.sha256(path.read_bytes()).hexdigest() == status['outputs'][str(path.relative_to(evidence.root))])
    evidence.own(status_path)
    evidence.own(path)
    return load_npz(path)


def difference(first, second):
    with localcontext() as context:
        context.prec = 64
        return np.asarray(first-second, float)


def save_step(evidence, name, coordinates, momenta, rates, current, history):
    path = evidence.output/(name+'.npz')
    np.savez_compressed(path, coordinates=np.array(coordinates, dtype=str), momenta=np.array(momenta, dtype=str),
        midpoint_rates=rates, midpoint_force=current['force'], midpoint_momentum=current['momentum'],
        radial_edges=current['solver'].edges, radial_nodes=current['solver'].nodes, metric=current['solution']['state'],
        force_decimal=np.array(current['force_decimal'], dtype=str), iterations=np.array([row['relative_residual'] for row in history]))
    evidence.own(path, 'outputs')


def main():
    evidence = EvidenceRun('annular-candidate-coupled-midpoint-attempt01', __file__)
    started = perf_counter()
    deadline = started+10000
    try:
        prior_path = evidence.output.parent/'annular-candidate-coordinate-covectors-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('force_and_envelope_gates_precede_evolution', prior['state'] == 'complete'
            and prior['full_coordinate_covectors_computed'] and prior['coordinate_envelope_qualified']
            and prior['quadrature_qualified'] and not prior['full_GR_limit_proven'])
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
            original_live_action_unchanged=True, new_coupled_evolution=False, modes_deleted=False,
            physical_force_mismatch_fixed=False, spatial_convergence_proven=False,
            full_live_P2_force_convergence_proven=False, general_nonzero_shift_or_temporal_current_derived=False,
            exact_finite_label_Galerkin_evolution_qualified=False, global_stability_proven=False,
            trajectories_qualified=False, horizon=1e-7, horizon_has_no_seconds_assignment=True,
            reference_order=10, material_order=32, radial_degree=22, radial_label_order=28,
            initial_checks=[], iterations=[], refinement=[], reversals=[], arithmetic=[], cases=[],
            precision_digits=64, common_state_not_projected_to_native=True,
            gravity_resolved_at_every_trial=True, momentum_and_force_same_reference_material_rule=True,
            full_saved_mass_is_preconditioner_only=True, absolute_velocity_correction_tolerance=2e-12,
            relative_nonlinear_residual_tolerance=5e-12, temporal_signal_relative_tolerance=2e-3)
        for branch in ['reference', 'MTS']:
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, unused_coordinates, rates = common_material(native, saved, packet)
            with localcontext() as context:
                context.prec = 64
                fields = apply_rational_rows(packet['embeddings'][0], decimal_array(saved['coordinates'][:, :-1].T)).T
                initial_coordinates = np.column_stack([fields, decimal_array(saved['coordinates'][:, -1])])
            for extension in (['reference'] if branch == 'reference' else ['primary', 'alternative']):
                case = branch+'-'+extension
                action_packet = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
                evaluator = LiveCommonEvaluation(owner, packet['overlay'], action_packet, extension, deadline)
                preconditioner = BandedSourceInverse(saved_matrix(evidence, case+'-22-fixed-metric-mass.npz'), rates.shape)
                evidence.check(case+'_all_preconditioner_directions_retained', preconditioner.count == 16425
                    and preconditioner.minimum_diagonal > 0 and preconditioner.minimum_schur_eigenvalue > 0)
                print(json.dumps(dict(case=case, operation='initial_common_state_momentum_force_check', seconds=perf_counter()-started)), flush=True)
                initial = evaluator.evaluate(initial_coordinates, rates)
                old_force = checked_load(evidence, 'annular-candidate-coordinate-covectors-attempt01', case+'-10-32-covectors.npz')
                old_momentum = checked_load(evidence, 'annular-candidate-live-momenta-attempt01', case+'-22-canonical.npz')['momentum']
                force_errors = {name:scaled_error(initial[name], old_force[name].T) for name in ['bulk', 'gram', 'dust']}
                momentum_error = preconditioner.residual_norm(initial['momentum']-old_momentum)/preconditioner.residual_norm(old_momentum)
                evidence.check(case+'_initial_force_agrees_with_sealed_action', max(force_errors.values()) < 2e-5, force_errors)
                evidence.check(case+'_independent_radial_and_material_momentum_rules_agree', momentum_error < 2e-5, momentum_error)
                evidence.report['initial_checks'].append(dict(branch=branch, extension=extension,
                    momentum_rule_relative_difference=momentum_error, force_relative_differences=force_errors,
                    valid_for_claim=False))
                initial_momenta = decimal_array(initial['momentum'])
                save_step(evidence, case+'-initial', initial_coordinates, initial_momenta, rates, initial, [])
                endpoints = {}

                def trajectory(label, coordinates, momenta, seed, steps, count, precision):
                    evaluator.precision = precision
                    histories = []
                    for index in range(count):
                        step_name = case+'-'+label+'-step'+str(index+1)
                        def record(row, midpoint, trial_rates, current, residual):
                            evidence.report['iterations'].append(dict(case=step_name, **row, valid_for_claim=False))
                            evidence.report['progress'] = dict(case=step_name, iteration=row['iteration'],
                                relative_residual=row['relative_residual'], maximum_correction=row['maximum_correction'],
                                seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                            recovery = evidence.output/'latest-trial-recovery.npz'
                            np.savez_compressed(recovery, coordinates=np.array(coordinates, dtype=str),
                                momenta=np.array(momenta, dtype=str), midpoint=np.array(midpoint, dtype=str),
                                rates=trial_rates, residual=residual, force=current['force'], metric=current['solution']['state'])
                        coordinates, momenta, seed, current, history = midpoint_step(evaluator, coordinates, momenta, seed,
                            steps, preconditioner, record)
                        save_step(evidence, step_name, coordinates, momenta, seed, current, history)
                        final = history[-1]
                        evidence.check(step_name+'_nonlinear_radial_and_chart_gates', final['relative_residual'] < 5e-12
                            and final['maximum_correction'] < 2e-12 and final['radial_residual'] < 2e-12
                            and final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
                        evidence.report['cases'].append(dict(branch=branch, extension=extension, label=label,
                            index=index+1, step=steps, digits=precision, full_components=16425, iterations=len(history),
                            **{name:final[name] for name in ['relative_residual', 'maximum_correction', 'radial_residual',
                                'minimum_F', 'maximum_speed_ratio']}, valid_for_claim=False))
                        histories.append(history)
                    return coordinates, momenta, seed, histories

                for count in [1, 2, 4]:
                    endpoints[count] = trajectory('forward'+str(count), initial_coordinates.copy(), initial_momenta.copy(),
                        rates.copy(), 1e-7/count, count, 64)
                reverse = trajectory('reverse', endpoints[1][0].copy(), endpoints[1][1].copy(), endpoints[1][2].copy(), -1e-7, 1, 64)
                alternate = trajectory('digits40', initial_coordinates.copy(), initial_momenta.copy(), rates.copy(), 1e-7, 1, 40)
                for component, initial_state in [(0, initial_coordinates), (1, initial_momenta)]:
                    for block, section in [('field', slice(None, -1)), ('source', slice(-1, None))]:
                        coarse = float(np.max(abs(difference(endpoints[1][component][:, section], endpoints[2][component][:, section]))))
                        fine = float(np.max(abs(difference(endpoints[2][component][:, section], endpoints[4][component][:, section]))))
                        signal = float(np.max(abs(difference(endpoints[4][component][:, section], initial_state[:, section]))))
                        scale = max(float(np.max(abs(np.asarray(initial_state[:, section], float)))), 1e-30)
                        floor = (2e-15 if component == 0 else 5e-12)*scale
                        tolerance = 2e-3*signal+floor
                        evidence.report['refinement'].append(dict(branch=branch, extension=extension, component=component,
                            block=block, coarse_difference=coarse, fine_difference=fine, motion_signal=signal,
                            refinement_ratio=fine/max(coarse, 1e-90), signal_relative_difference=fine/max(signal, 1e-90),
                            roundoff_floor=floor, tolerance=tolerance, passed=fine < tolerance,
                            not_spatial_or_global_stability_claim=True, valid_for_claim=False))
                        error = float(np.max(abs(difference(reverse[component][:, section], initial_state[:, section]))))
                        reverse_tolerance = (2e-14 if component == 0 else 2e-10)*scale
                        evidence.report['reversals'].append(dict(branch=branch, extension=extension, component=component,
                            block=block, maximum_error=error, tolerance=reverse_tolerance,
                            passed=error < reverse_tolerance, valid_for_claim=False))
                        precision_error = float(np.max(abs(difference(alternate[component][:, section], endpoints[1][component][:, section]))))
                        evidence.report['arithmetic'].append(dict(branch=branch, extension=extension, component=component,
                            block=block, maximum_difference=precision_error, tolerance=reverse_tolerance,
                            passed=precision_error < reverse_tolerance, numerical_not_physical_precision=True, valid_for_claim=False))
                evidence.save()
                print(json.dumps(dict(case=case, operation='branch_complete', evaluations=evaluator.evaluations,
                    seconds=perf_counter()-started)), flush=True)
        recovery = evidence.output/'latest-trial-recovery.npz'
        if recovery.exists():
            evidence.own(recovery, 'outputs')
        evidence.report.update(new_coupled_evolution=True,
            trajectories_qualified=all(row['passed'] for key in ['refinement', 'reversals', 'arithmetic'] for row in evidence.report[key]),
            seconds=perf_counter()-started)
        evidence.check('all_branches_all_pilots_retained', len(evidence.report['cases']) == 27
            and all(len(evidence.report[key]) == 12 for key in ['refinement', 'reversals', 'arithmetic']))
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']),
            qualified=evidence.report['trajectories_qualified'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        recovery = evidence.output/'latest-trial-recovery.npz'
        if recovery.exists():
            evidence.own(recovery, 'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
