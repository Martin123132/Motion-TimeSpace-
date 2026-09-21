from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_midpoint_20260921 import LiveCommonEvaluation
from annular_candidate_anderson_midpoint_v2_20260921 import midpoint_step
from annular_endpoint_legendre_inverse_20260921 import endpoint_inverse
from annular_candidate_hamiltonian_20260921 import decimals, energy_channels
from derive_annular_candidate_midpoint_20260921 import saved_matrix, save_step, difference
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import contextlib
import json
import hashlib
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--horizon', choices=['1e-5'], default='1e-5')
    parser.add_argument('--attempt', default='01')
    parser.add_argument('--resume', default='annular-candidate-finer-time-attempt01')
    parser.add_argument('--max-seconds', type=float, default=6600)
    args = parser.parse_args()
    args.controls = True
    horizon = float(args.horizon)
    evidence = EvidenceRun('annular-candidate-fine16-quadrature-attempt'+args.attempt, __file__)
    started = perf_counter()
    deadline = started+args.max_seconds
    try:
        prior_path = evidence.output.parent/'annular-candidate-longer-evolution-v2-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('completed_energy_source', prior['state'] == 'complete' and prior['energy_smoke_passed']
            and all(row['passed'] for row in prior['checks']))
        control_path = evidence.output.parent/'annular-candidate-accelerated-midpoint-control-attempt02/status.json'
        control = json.loads(control_path.read_text())
        evidence.own(control_path)
        evidence.check('accelerated_solver_independent_linear_control', control['state'] == 'complete'
            and all(row['passed'] for row in control['checks']))
        evidence.report.update(midpoint_solver='full_residual_history_acceleration', history_only_not_physical_mode_reduction=True)
        energy_path = evidence.output.parent/'annular-candidate-endpoint-energy-attempt03/status.json'
        energy_source = json.loads(energy_path.read_text())
        evidence.own(energy_path)
        evidence.report.update(horizon=horizon, horizon_label=args.horizon, controls=args.controls, matched_quadrature_steps=16, reverse_control_repeated=False,
            maximum_seconds=args.max_seconds, horizon_has_no_seconds_assignment=True,
            github_action=False, subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
            original_live_action_unchanged=True, modes_deleted=False, new_coupled_evolution=False,
            full_saved_mass_is_preconditioner_only=True, gravity_resolved_at_every_trial=True,
            common_state_not_projected_to_native=True, momentum_and_force_same_reference_material_rule=True,
            temporal_signal_relative_tolerance=2e-3, energy_relative_smoke_tolerance=1e-9,
            trajectories_qualified=False, energy_smoke_passed=False, energy_time_order_resolved=False,
            physical_force_mismatch_fixed=False, spatial_convergence_proven=False, global_stability_proven=False,
            total_energy_conservation_proven=False, initial_sources=[], iterations=[], endpoints=[],
            refinement=[], energy_refinement=[], quadrature=[], reversals=[])
        resume_path = evidence.output.parent/args.resume/'status.json'
        resume = json.loads(resume_path.read_text())
        evidence.own(resume_path)
        evidence.check('source_is_saved_resumable_execution', resume['state'] in ['complete', 'failed']
            and all(row['passed'] for row in resume['checks']))
        evidence.report.update(resumed_from=str(resume_path.relative_to(evidence.root)),
            reused_steps=0, reused_endpoints=0, reused_iterations_not_counted_as_new=True,
            iteration_cap=96, history_vectors=40)
        def load_resume(path):
            key = str(path.relative_to(evidence.root))
            expected = resume['outputs'].get(key, resume['inputs'].get(key))
            evidence.check(path.name+'_resume_hash', expected is not None and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
            evidence.own(path)
            with np.load(path, allow_pickle=False) as data:
                return {key:data[key].copy() for key in data.files}
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, unused, unused_rates = common_material(native, saved, packet)
            action = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
            initial = checked_load(evidence, 'annular-candidate-coupled-midpoint-attempt01', case+'-initial.npz')
            coordinates, momenta, rates = decimals(initial['coordinates']), decimals(initial['momenta']), initial['midpoint_rates']
            preconditioner = BandedSourceInverse(saved_matrix(evidence, case+'-22-fixed-metric-mass.npz'), rates.shape)
            evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline)
            evidence.check(case+'_all_mass_directions_retained', preconditioner.count == 16425
                and preconditioner.minimum_diagonal > 0 and preconditioner.minimum_schur_eigenvalue > 0)
            initial_path = evidence.output.parent/'annular-candidate-coupled-midpoint-attempt01'/(case+'-initial.npz')
            evidence.report['initial_sources'].append(dict(branch=branch, extension=extension,
                path=str(initial_path.relative_to(evidence.root)), valid_for_claim=False))

            def recorder(name, position, momentum):
                def record(row, midpoint, trial_rates, current, residual):
                    evidence.report['iterations'].append(dict(case=name, **row, valid_for_claim=False))
                    evidence.report['progress'] = dict(case=name, iteration=row['iteration'],
                        relative_residual=row['relative_residual'], maximum_correction=row['maximum_correction'],
                        seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                    np.savez_compressed(evidence.output/'latest-trial-recovery.npz',
                        coordinates=np.array(position, dtype=str), momenta=np.array(momentum, dtype=str),
                        midpoint=np.array(midpoint, dtype=str), rates=trial_rates, residual=residual,
                        force=current['force'], metric=current['solution']['state'])
                return record

            def gates(name, history):
                final = history[-1]
                evidence.check(name+'_solver_and_chart', final['relative_residual'] < 5e-12
                    and final['maximum_correction'] < 2e-12 and final['radial_residual'] < 2e-12
                    and final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
                return {key:final[key] for key in ['relative_residual', 'maximum_correction', 'radial_residual',
                    'minimum_F', 'maximum_speed_ratio']}

            def trajectory(label, position, momentum, seed, count, duration, engine, previous):
                for index in range(count):
                    name = case+'-'+label+'-step'+str(index+1)
                    previous_row = next((item for item in resume['cases'] if item['branch'] == branch
                        and item['extension'] == extension and item['label'] == label and item['index'] == index+1), None)
                    if previous_row is not None:
                        before = load_resume(evidence.root/previous_row['previous_path'])
                        saved_step = load_resume(evidence.root/previous_row['path'])
                        evidence.check(name+'_resume_initial_state_exact', np.array_equal(position, decimals(before['coordinates']))
                            and np.array_equal(momentum, decimals(before['momenta'])) and previous_row['step'] == duration/count)
                        position, momentum, seed = decimals(saved_step['coordinates']), decimals(saved_step['momenta']), saved_step['midpoint_rates']
                        previous = evidence.root/previous_row['path']
                        evidence.report['cases'].append(dict(previous_row, reused=True))
                        evidence.report['reused_steps'] += 1
                        evidence.save()
                        continue
                    restarted = False
                    if resume.get('progress', {}).get('case') == name:
                        trial = load_resume(resume_path.parent/'latest-trial-recovery.npz')
                        evidence.check(name+'_restart_same_q_p', np.array_equal(position, decimals(trial['coordinates']))
                            and np.array_equal(momentum, decimals(trial['momenta'])))
                        seed = trial['rates'].copy()
                        restarted = True
                    position, momentum, seed, current, history = midpoint_step(engine, position, momentum, seed,
                        duration/count, preconditioner, recorder(name, position, momentum))
                    save_step(evidence, name, position, momentum, seed, current, history)
                    path = evidence.output/(name+'.npz')
                    evidence.report['cases'].append(dict(branch=branch, extension=extension, label=label,
                        index=index+1, step=duration/count, digits=64, full_components=16425, iterations=len(history),
                        reused=False, restarted_from_failed_trial=restarted,
                        path=str(path.relative_to(evidence.root)), previous_path=str(previous.relative_to(evidence.root)),
                        **gates(name, history), valid_for_claim=False))
                    previous = path
                    evidence.save()
                return position, momentum, seed, previous

            def endpoint_energy(label, endpoint, engine, baseline_label):
                position, momentum, seed, source_path = endpoint
                name = case+'-'+label+'-endpoint'
                previous_row = next((item for item in resume['endpoints'] if item['branch'] == branch
                    and item['extension'] == extension and item['label'] == label), None)
                if previous_row is not None:
                    saved_energy = load_resume(evidence.root/previous_row['path'])
                    evidence.check(name+'_resume_energy_state_exact', np.array_equal(position, decimals(saved_energy['coordinates']))
                        and np.array_equal(momentum, decimals(saved_energy['target_momenta'])) and previous_row['baseline_label'] == baseline_label)
                    row = dict(previous_row, reused=True)
                    evidence.report['endpoints'].append(row)
                    evidence.report['reused_endpoints'] += 1
                    evidence.save()
                    return row
                recovered_q, recovered_p, velocity, current, history = endpoint_inverse(engine,
                    position, momentum, seed, preconditioner, recorder(name, position, momentum))
                evidence.check(name+'_fixed_state', np.array_equal(position, recovered_q) and np.array_equal(momentum, recovered_p))
                diagnostics = gates(name, history)
                energy, numeric, raw = energy_channels(current, momentum, velocity, preconditioner)
                baseline = next(row for row in energy_source['cases'] if row['branch'] == branch
                    and row['extension'] == extension and row['label'] == baseline_label)
                with localcontext() as context:
                    context.prec = 64
                    base = Decimal(baseline['energy']['full_shifted_hamiltonian'])
                    full = Decimal(energy['full_shifted_hamiltonian'])
                    drift = full-base
                    boundary = Decimal(energy['boundary_integral'])
                floor = float(numeric['diagnostic_resolution_scale']+baseline['diagnostic_resolution_scale'])
                evidence.check(name+'_Legendre_and_inverse_energy', float(abs(full-boundary)/abs(boundary)) < 2e-9
                    and numeric['pointwise_radial_Legendre_relative_defect'] < 2e-12
                    and abs(float(energy['inverse_energy_error'])) <= numeric['inverse_energy_Cauchy_bound']*(1+1e-10)+1e-30)
                path = evidence.output/(name+'-energy-inputs.npz')
                np.savez_compressed(path, **raw, coordinates=np.array(position, dtype=str), seed_rates=seed)
                evidence.own(path, 'outputs')
                row = dict(branch=branch, extension=extension, label=label, path=str(path.relative_to(evidence.root)),
                    source_state=str(source_path.relative_to(evidence.root)), baseline_label=baseline_label,
                    full_components=16425, iterations=len(history), **diagnostics, **numeric, energy=energy,
                    energy_drift=str(drift), relative_energy_drift=float(abs(drift)/abs(base)),
                    paired_diagnostic_resolution=floor, drift_resolved=bool(abs(float(drift)) > 4*floor),
                    smoke_passed=bool(abs(drift) < Decimal('1e-9')*abs(base)), valid_for_claim=False)
                evidence.report['endpoints'].append(row)
                evidence.save()
                return row

            endpoints, energy_rows = {}, {}
            for count in [16]:
                label = 'forward'+str(count)
                endpoints[count] = trajectory(label, coordinates.copy(), momenta.copy(), rates.copy(), count,
                    horizon, evaluator, initial_path)
                energy_rows[count] = endpoint_energy(label, endpoints[count], evaluator, 'initial')
            if args.controls:
                fine_initial = checked_load(evidence, 'annular-candidate-midpoint-quadrature-attempt01', case+'-initial.npz')
                fine_q, fine_p, fine_rates = decimals(fine_initial['coordinates']), decimals(fine_initial['momenta']), fine_initial['midpoint_rates']
                evidence.check(case+'_fine_physical_initial_state_matches', np.array_equal(fine_q, coordinates) and np.array_equal(fine_rates, rates))
                fine_evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline,
                    reference_order=16, material_order=48)
                fine_path = evidence.output.parent/'annular-candidate-midpoint-quadrature-attempt01'/(case+'-initial.npz')
                finer = trajectory('fine', fine_q, fine_p, fine_rates.copy(), 16, horizon, fine_evaluator, fine_path)
                endpoint_energy('fine', finer, fine_evaluator, 'fine_initial')
                for component, base, fine_base in [(0, coordinates, fine_q), (1, momenta, fine_p)]:
                    for block, section in [('field', slice(None, -1)), ('source', slice(-1, None))]:
                        increments = difference(endpoints[16][component][:, section], base[:, section])
                        error = float(np.max(abs(difference(finer[component][:, section], fine_base[:, section])-increments)))
                        signal = float(np.max(abs(increments)))
                        scale = max(float(np.max(abs(np.asarray(base[:, section], float)))), 1e-30)
                        tolerance = 2e-3*signal+(2e-15 if component == 0 else 5e-12)*scale
                        evidence.report['quadrature'].append(dict(branch=branch, extension=extension, component=component,
                            block=block, increment_difference=error, motion_signal=signal, tolerance=tolerance,
                            signal_relative_difference=error/max(signal, 1e-90), passed=bool(error < tolerance), valid_for_claim=False))
            evidence.save()
        evidence.own(evidence.output/'latest-trial-recovery.npz', 'outputs')
        evidence.check('equal_branch_counts', len(evidence.report['cases']) == 96
            and len(evidence.report['endpoints']) == 6
            and len(evidence.report['refinement']) == 0 and len(evidence.report['energy_refinement']) == 0
            and len(evidence.report['quadrature']) == 12
            and len(evidence.report['reversals']) == 0)
        evidence.report.update(new_coupled_evolution=True,
            new_accepted_steps=sum(not row.get('reused', False) for row in evidence.report['cases']),
            new_trial_evaluations=len(evidence.report['iterations']),
            prior_iteration_histories_preserved_in_source=True,
            trajectories_qualified=all(row['passed'] for key in ['refinement', 'quadrature', 'reversals'] for row in evidence.report[key]),
            energy_smoke_passed=all(row['smoke_passed'] for row in evidence.report['endpoints']),
            energy_time_order_resolved=False, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps({key:evidence.report[key] for key in ['state', 'horizon', 'trajectories_qualified', 'energy_smoke_passed', 'seconds']}), flush=True)
    except Exception as error:
        recovery = evidence.output/'latest-trial-recovery.npz'
        if recovery.exists():
            evidence.own(recovery, 'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
