from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_live_exponential_20260919 import FrozenCanonicalSplit, exponential_midpoint
from annular_P2_bulk_refinement_20260919 import gram_jump_split
from annular_P2_graded_source_20260919 import scalar_pencil
from run_annular_P2_evolved_source_halving_20260919 import force_data
from run_annular_P2_continuum_bridge_20260918 import checked_load
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from compare_annular_P2_continuum_bridge_20260918 import physical_comparison
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-bulk513-evolution-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, base_count=513, source_cap=1e-5,
            duration=4e-5, steps=[32, 64], maximum_wall_seconds=6000.,
            initial_preparation_unchanged=True, full_Gram_source_geometry_retained=True,
            all_scalar_modes_retained=True, previous_point004_window_not_retested=True,
            two_spatial_resolutions_not_convergence_theorem=True,
            time_force_budget=2e-9, time_state_budget=1e-6,
            endpoint_force_threshold=2.700598122731542e-8)
        folder = 'annular-P2-bulk513-preflight-'+args.branch+'-attempt01'
        preflight_path = evidence.output.parent/folder/'status.json'
        preflight = json.loads(preflight_path.read_text())
        evidence.own(preflight_path)
        evidence.check('initial_cost_and_physics_preflight', preflight['state'] == 'complete'
            and all(row['passed'] for row in preflight['checks']) and preflight['forward_candidate_allowed'])
        data = checked_load(evidence, folder, 'initial.npz')
        initial = np.stack([data['coordinates'], data['momenta']])
        system = IndexedGradedP2System(513, args.branch == 'MTS', 1e-5)
        rates, geometry = system.solve(*initial)
        split = FrozenCanonicalSplit(system, initial, geometry)
        split.started, split.maximum_wall_seconds = started, evidence.report['maximum_wall_seconds']
        evidence.report['factor_diagnostics'] = split.factor_diagnostics
        evidence.check('all_full_scalar_modes_retained', split.frequency.shape == (15, system.count+1)
            and np.all(split.frequency[:, :-1] > 0) and np.all(split.frequency[:, -1] == 0))
        evidence.check('modal_mass_and_backward_residual',
            max(row['mass_orthogonality'] for row in split.factor_diagnostics) < 2e-12
            and max(row['normwise_backward_residual'] for row in split.factor_diagnostics) < 2e-11)
        delta = np.random.default_rng(20260919).normal(size=initial.shape)*1e-8
        roundtrip = float(np.linalg.norm(split.decode(split.encode(delta))-delta)/np.linalg.norm(delta))
        evidence.check('new_grid_modal_roundtrip', roundtrip < 2e-11, roundtrip)
        initial_flow = np.stack([rates, system.forces(initial[0], rates, geometry)])
        first_remainder = split.encode(initial_flow)
        error = float(np.linalg.norm(split.decode(first_remainder)-initial_flow)/np.linalg.norm(initial_flow))
        evidence.check('initial_full_rhs_not_truncated', error < 2e-10, error)
        basis_path = evidence.output/'frozen-canonical-basis.npz'
        np.savez_compressed(basis_path, frequency=split.frequency, modes=np.array(split.modes),
            mass_modes=np.array(split.mass_modes), initial=initial)
        evidence.own(basis_path, 'outputs')
        oracle_data = checked_load(evidence, 'annular-P2-live-exponential-short-continuum-attempt01', 'continuum512.npz')
        oracle = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        unused, target, forces = oracle.rhs_with_geometry(oracle_data['state'])
        target_force = float(forces['radiation'][4])
        baseline_name = 'annular-P2-evolved-source-halving-'+args.branch+'-attempt'+('02' if args.branch == 'MTS' else '01')
        baseline_path = evidence.output.parent/baseline_name/'status.json'
        baseline = json.loads(baseline_path.read_text())
        evidence.own(baseline_path)
        evidence.check('paired_coarse_endpoint_complete', baseline['state'] == 'complete'
            and baseline['duration'] == evidence.report['duration'] and baseline['empirical_time_budget_pass']
            and baseline['continuum_force'] == target_force)
        print(json.dumps(dict(branch=args.branch, phase='all_mode_preflight_done',
            seconds=perf_counter()-started, maximum_frequency=float(np.max(split.frequency)))), flush=True)
        endpoints = []
        for steps in evidence.report['steps']:
            values = np.zeros_like(initial)
            states = [initial.copy()]
            step = evidence.report['duration']/steps
            evolution_started = perf_counter()
            for index in range(steps):
                values = exponential_midpoint(split, values, step, first_remainder=first_remainder if index == 0 else None)
                state = split.physical(values)
                if not np.all(np.isfinite(state)):
                    raise RuntimeError('Nonfinite bulk-refined state.')
                states.append(state.copy())
                path = evidence.output/('steps'+str(steps)+'-accepted'+str(index+1).zfill(3)+'.npz')
                np.savez_compressed(path, time=(index+1)*step, state=state, modal_increment=values)
                evidence.own(path, 'outputs')
                evidence.report.update(active_steps=steps, accepted=index+1, accepted_time=(index+1)*step,
                    seconds=perf_counter()-started, evaluations=split.evaluations)
                evidence.save()
                if (index+1) % 8 == 0:
                    print(json.dumps(dict(branch=args.branch, steps=steps, accepted=index+1,
                        seconds=perf_counter()-started)), flush=True)
            evolution_seconds = perf_counter()-evolution_started
            tangent, diagnostic = force_data(system, state)
            comparison = physical_comparison(system, state[0], tangent.rates, tangent.geometry, oracle, target)
            current = tangent.layer_data(0.)
            mass, unused = scalar_pencil(current.layer, current.coordinates)
            gram = gram_jump_split(current.layer, current.coordinates, mass)
            force = diagnostic['lift']['force']
            force_error = abs(force-target_force)
            lapse, root = tangent.geometry.metric(state[0, :, -1])
            timelike = float(np.max(abs(tangent.rates[:, -1]/(lapse*root))))
            row = dict(steps=steps, force=force, force_error=force_error,
                instantaneous_relative_force_error=force_error/abs(target_force),
                peak_scaled_force_gate_pass=bool(force_error <= evidence.report['endpoint_force_threshold']),
                maximum_rotation_angle=float(step*np.max(split.frequency)), evolution_seconds=evolution_seconds,
                gram_split=gram, **diagnostic, **comparison)
            evidence.report['cases'].append(row)
            evidence.save()
            evidence.check('steps'+str(steps)+'_constraints', diagnostic['canonical'] < 2e-11
                and max(diagnostic['radial']) < 2e-9)
            evidence.check('steps'+str(steps)+'_force_and_current_identities', diagnostic['lift']['identity_error'] < 2e-9
                and diagnostic['schur']['force_identity_error'] < 2e-9 and diagnostic['noether']['residual'] < 2e-9
                and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
            evidence.check('steps'+str(steps)+'_regular_domain', tangent.material.minimum_jacobian > 0 and timelike < 1)
            path = evidence.output/('trajectory-steps'+str(steps)+'.npz')
            np.savez_compressed(path, times=np.linspace(0., evidence.report['duration'], steps+1),
                states=np.array(states), final_modal_increment=values)
            evidence.own(path, 'outputs')
            endpoints.append(values.copy())
            print(json.dumps(dict(branch=args.branch, steps=steps, force=force, force_error=force_error,
                seconds=perf_counter()-started)), flush=True)
        time_force = abs(evidence.report['cases'][0]['force']-evidence.report['cases'][1]['force'])
        time_state = split.relative_energy_difference(*endpoints)
        final = evidence.report['cases'][-1]
        time_pass = time_force < evidence.report['time_force_budget'] and time_state < evidence.report['time_state_budget']
        material_pass = final['source_error'] < 5e-7 and final['velocity_error'] < 2e-5 and final['clock_rate_error'] < 2e-7
        evidence.report.update(continuum_force=target_force, baseline_force=baseline['refined_force'],
            baseline_force_error=baseline['refined_force_error'], baseline_time_force_difference=baseline['time_force_difference'],
            coarse_endpoint=baseline['cases'][-1], refined_force=final['force'], refined_force_error=final['force_error'],
            force_error_ratio=final['force_error']/baseline['refined_force_error'],
            time_force_difference=time_force, time_state_difference=time_state, empirical_time_budget_pass=bool(time_pass),
            scoped_endpoint_gate_pass=bool(time_pass and material_pass and final['field_error'] < .005
                and final['peak_scaled_force_gate_pass']), seconds=perf_counter()-started,
            independent_time_integrator_on_this_grid_not_yet_run=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', branch=args.branch, ratio=evidence.report['force_error_ratio'],
            time_pass=bool(time_pass), endpoint_pass=evidence.report['scoped_endpoint_gate_pass'],
            seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
