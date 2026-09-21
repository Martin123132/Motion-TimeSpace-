from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedP2System
from annular_P2_live_exponential_20260919 import FrozenCanonicalSplit, exponential_midpoint
from run_annular_P2_continuum_bridge_20260918 import checked_load
from annular_live_P2_current_20260918 import LiveP2Tangent
from scipy.linalg import solve
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def diagnostics(system, state):
    coordinates, momenta = state
    tangent = LiveP2Tangent(system, coordinates, momenta)
    current = tangent.layer_data(0.)
    radial = tangent.geometry.off_grid_residual(tangent.rates)
    lapse, root = tangent.geometry.metric(coordinates[:, -1])
    clock = np.sqrt(lapse**2-tangent.rates[:, -1]**2/root**2)
    return dict(reduced_wave_force=float(-current.wave_source_euler),
        canonical_residual=system.canonical_residual(coordinates, momenta, tangent.rates, tangent.geometry),
        radial_residual=[float(value) for value in radial],
        source_positions=coordinates[:, -1].tolist(), source_rates=tangent.rates[:, -1].tolist(),
        proper_clock_rates=clock.tolist(), noether=current.noether(),
        minimum_material_jacobian=float(tangent.material.minimum_jacobian),
        maximum_timelike_ratio=float(np.max(abs(tangent.rates[:, -1]/(lapse*root)))),
        exterior_mass=float(tangent.geometry.mass_nodes[-1, -1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-live-exponential-'+args.branch+'-257-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, all_scalar_modes_retained=True,
            live_geometry_recomputed_at_every_nonlinear_stage=True, live_source_and_Gram_terms_retained=True,
            original_canonical_momenta_used=True, initial_preparation_unchanged=True,
            exact_remainder_not_frozen_geometry_evolution=True, duration=4e-5,
            steps=[4, 8, 16], time_force_diagnostic_budget=2e-9,
            time_modal_relative_budget=1e-6, continuum_accuracy_claim=False,
            time_refinement_not_uniform_error_certificate=True, maximum_wall_seconds=7200.)
        prerequisite = evidence.output.parent/'annular-P2-live-exponential-algebra-attempt02/status.json'
        status = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('solver_algebra_preflight_complete', status['state'] == 'complete'
            and all(row['passed'] for row in status['checks']))
        data = checked_load(evidence, 'annular-P2-joint-refinement-257-cap4e-05-attempt01', args.branch+'-initial.npz')
        system = GradedP2System(257, args.branch == 'MTS', 4e-5)
        initial = np.stack([data['coordinates'], data['momenta']])
        rates, geometry = system.solve(*initial)
        split = FrozenCanonicalSplit(system, initial, geometry)
        split.started = started
        evidence.report['factor_diagnostics'] = split.factor_diagnostics
        evidence.check('all_layer_modes_retained', split.frequency.shape == (15, 555)
            and np.all(split.frequency[:, :-1] > 0) and np.all(split.frequency[:, -1] == 0))
        evidence.check('all_layer_mass_orthogonality', max(row['mass_orthogonality'] for row in split.factor_diagnostics) < 2e-12)
        evidence.check('all_layer_backward_residual', max(row['normwise_backward_residual']
            for row in split.factor_diagnostics) < 2e-11)
        rng = np.random.default_rng(20260919)
        delta = rng.normal(size=initial.shape)*1e-8
        roundtrip = float(np.linalg.norm(split.decode(split.encode(delta))-delta)/np.linalg.norm(delta))
        evidence.check('canonical_increment_roundtrip', roundtrip < 2e-11, roundtrip)
        delta[:, :, -1] = 0.
        physical_linear = np.zeros_like(delta)
        for index, (mass, stiffness) in enumerate(split.pencils):
            physical_linear[0, index, :-1] = solve(mass, delta[1, index, :-1], assume_a='pos', check_finite=False)
            physical_linear[1, index, :-1] = -stiffness @ delta[0, index, :-1]
        reconstructed = split.decode(split.linear(split.encode(delta)))
        pencil_error = float(np.linalg.norm(reconstructed-physical_linear)/np.linalg.norm(physical_linear))
        evidence.check('canonical_pencil_action_independent_mass_solve', pencil_error < 2e-9, pencil_error)
        zero = np.zeros_like(initial)
        initial_live = split.live(zero)
        perturbation = 2e-6*initial_live
        for tag, values in [('initial', zero), ('perturbed', perturbation)]:
            direct = system.rhs(0., split.physical(values).ravel()).reshape(initial.shape)
            remainder = initial_live if tag == 'initial' else split.remainder(values)
            recovered = split.decode(split.linear(values)+remainder)
            error = float(np.linalg.norm(recovered-direct)/max(np.linalg.norm(direct), 1e-30))
            source_error = float(np.max(abs(recovered[:, :, -1]-direct[:, :, -1])))
            dropped_error = float(np.linalg.norm(split.decode(split.linear(values))-direct))
            evidence.check(tag+'_full_RHS_reconstructed', error < 2e-10 and source_error < 2e-14,
                dict(relative_error=error, source_error=source_error))
            evidence.check(tag+'_omitted_remainder_control_detected', dropped_error > 1e-6, dropped_error)
            evidence.check(tag+'_source_live_not_silenced', np.max(abs(direct[:, :, -1])) > 1e-6)
        basis_path = evidence.output/'frozen-canonical-basis.npz'
        np.savez_compressed(basis_path, frequency=split.frequency, modes=np.array(split.modes),
            mass_modes=np.array(split.mass_modes), initial=initial)
        evidence.own(basis_path, 'outputs')
        print(json.dumps(dict(branch=args.branch, phase='live_preflight_complete', seconds=perf_counter()-started)), flush=True)
        final_modes, final_states, end_diagnostics = [], [], []
        for steps in evidence.report['steps']:
            step = evidence.report['duration']/steps
            values = zero.copy()
            stages_started, starting_evaluations = perf_counter(), split.evaluations
            accepted = [initial.copy()]
            for index in range(steps):
                values = exponential_midpoint(split, values, step, first_remainder=initial_live if index == 0 else None)
                if not np.all(np.isfinite(values)):
                    raise ValueError('Nonfinite modal state; no successful-step marker emitted.')
                state = split.physical(values)
                accepted.append(state)
                path = evidence.output/('steps'+str(steps)+'-accepted'+str(index+1).zfill(3)+'.npz')
                np.savez_compressed(path, time=(index+1)*step, state=state, modal_increment=values)
                evidence.own(path, 'outputs')
                evidence.report.update(active_steps=steps, accepted_step=index+1,
                    accepted_time=(index+1)*step, evaluations=split.evaluations, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(dict(branch=args.branch, steps=steps, accepted=index+1,
                    time=(index+1)*step, evaluations=split.evaluations, seconds=perf_counter()-started)), flush=True)
            evolution_seconds = perf_counter()-stages_started
            diagnostic = diagnostics(system, state)
            row = dict(steps=steps, step=step, evolution_seconds=evolution_seconds,
                evolution_RHS_evaluations=split.evaluations-starting_evaluations,
                maximum_rotation_angle=float(step*np.max(split.frequency)), **diagnostic)
            evidence.report['cases'].append(row)
            evidence.save()
            evidence.check('steps'+str(steps)+'_constraints', diagnostic['canonical_residual'] < 2e-11
                and max(diagnostic['radial_residual']) < 2e-9, diagnostic)
            evidence.check('steps'+str(steps)+'_regular_domain', diagnostic['minimum_material_jacobian'] > 0
                and diagnostic['maximum_timelike_ratio'] < 1)
            evidence.check('steps'+str(steps)+'_current_and_Euler', diagnostic['noether']['residual'] < 2e-9
                and diagnostic['noether']['source_euler'] < 2e-8
                and diagnostic['noether']['scalar_euler'] < 2e-8, diagnostic['noether'])
            trajectory = evidence.output/('trajectory-steps'+str(steps)+'.npz')
            np.savez_compressed(trajectory, times=np.linspace(0., evidence.report['duration'], steps+1),
                states=np.array(accepted), final_modal_increment=values)
            evidence.own(trajectory, 'outputs')
            final_modes.append(values.copy())
            final_states.append(state.copy())
            end_diagnostics.append(diagnostic)
        comparisons = []
        for index in range(2):
            coarse, fine = end_diagnostics[index:index+2]
            force_change = abs(coarse['reduced_wave_force']-fine['reduced_wave_force'])
            modal_error = split.relative_energy_difference(final_modes[index], final_modes[index+1])
            comparisons.append(dict(coarse_steps=evidence.report['steps'][index], fine_steps=evidence.report['steps'][index+1],
                relative_frozen_energy_norm_difference=modal_error, force_difference=force_change,
                source_position_difference=float(np.max(abs(np.array(coarse['source_positions'])-fine['source_positions']))),
                clock_rate_difference=float(np.max(abs(np.array(coarse['proper_clock_rates'])-fine['proper_clock_rates']))),
                empirical_time_budget_pass=bool(force_change < evidence.report['time_force_diagnostic_budget']
                    and modal_error < evidence.report['time_modal_relative_budget'])))
        evidence.report.update(comparisons=comparisons,
            modal_difference_refinement_ratio=comparisons[0]['relative_frozen_energy_norm_difference']/
                max(comparisons[1]['relative_frozen_energy_norm_difference'], 1e-300),
            force_difference_refinement_ratio=comparisons[0]['force_difference']/max(comparisons[1]['force_difference'], 1e-300),
            empirical_final_time_budget_pass=comparisons[-1]['empirical_time_budget_pass'],
            total_RHS_evaluations=split.evaluations, total_RHS_seconds=split.rhs_seconds,
            seconds=perf_counter()-started, elapsed_horizon_fraction_of_previous_point004=.01)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(branch=args.branch, state='complete', checks=len(evidence.report['checks']),
            comparisons=comparisons, seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
