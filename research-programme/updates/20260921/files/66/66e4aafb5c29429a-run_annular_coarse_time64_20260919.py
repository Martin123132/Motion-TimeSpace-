from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_live_exponential_20260919 import FrozenCanonicalSplit, exponential_midpoint
from run_annular_P2_evolved_source_halving_v2_20260919 import force_data
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-coarse-time64-'+args.branch+'-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(branch=args.branch, github_action=False, subagents_used=False,
            no_new_evolution=False, new_short_live_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            initial_preparation_unchanged=True, original_action_and_source_unchanged=True,
            all_modes_retained=True, same_exponential_midpoint_integrator=True,
            fine_trajectory_fixed=True, base_count=257, source_cap=2e-5, duration=4e-5,
            steps=64, maximum_wall_seconds=3600., valid_for_claim=False)
        coarse_folder = 'annular-P2-evolved-source-halving-'+args.branch+'-attempt'+('02' if args.branch == 'MTS' else '01')
        old = checked_load(evidence, coarse_folder, 'steps32-accepted032.npz')
        coarse_status_path = evidence.output.parent/coarse_folder/'status.json'
        old_status = json.loads(coarse_status_path.read_text())
        old_case = next(row for row in old_status['cases'] if row['steps'] == 32)
        fine_folder = ('annular-P2-bulk513-MTS-time128-attempt01' if args.branch == 'MTS'
            else 'annular-P2-bulk513-evolution-reference-attempt01')
        fine_steps = 128 if args.branch == 'MTS' else 64
        fine = checked_load(evidence, fine_folder, 'trajectory-steps'+str(fine_steps)+'.npz')
        fine_status = json.loads((evidence.output.parent/fine_folder/'status.json').read_text())
        fine_case = next(row for row in fine_status['cases'] if row['steps'] == fine_steps)
        evidence.report.update(fixed_fine_folder=fine_folder, fixed_fine_steps=fine_steps,
            previous_coarse_folder=coarse_folder, fine_endpoint_force=fine_case['force'],
            continuum_force=old_status['continuum_force'])
        evidence.check('fine_and_coarse_comparators_same_endpoint',
            abs(float(old['time'])-4e-5) < 1e-17 and abs(float(fine['times'][-1])-4e-5) < 1e-17)
        evidence.check('same_continuum_comparator',
            abs(old_status['continuum_force']-fine_status['continuum_force']) < 1e-20)
        data = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', args.branch+'-initial.npz')
        initial = np.stack([data['coordinates'], data['momenta']])
        system = IndexedGradedP2System(257, args.branch == 'MTS', 2e-5)
        rates, geometry = system.solve(*initial)
        flow = np.stack([rates, system.forces(initial[0], rates, geometry)])
        split = FrozenCanonicalSplit(system, initial, geometry)
        split.started, split.maximum_wall_seconds = started, evidence.report['maximum_wall_seconds']
        evidence.report['factor_diagnostics'] = split.factor_diagnostics
        evidence.check('all_positive_scalar_modes_and_source_retained', system.count == 558
            and initial.shape == (2, 15, 559) and split.frequency.shape == (15, 559)
            and np.all(split.frequency[:, :-1] > 0) and np.all(split.frequency[:, -1] == 0))
        encoded_flow = split.encode(flow)
        roundtrip = float(np.max(abs(split.decode(encoded_flow)-flow)))
        evidence.check('initial_flow_roundtrip', roundtrip < 2e-10, roundtrip)
        basis_path = evidence.output/'frozen-canonical-basis.npz'
        np.savez_compressed(basis_path, frequency=split.frequency, modes=split.modes,
            mass_modes=split.mass_modes, initial=initial)
        evidence.own(basis_path, 'outputs')
        values = np.zeros_like(initial)
        states = [initial.copy()]
        step = evidence.report['duration']/evidence.report['steps']
        for index in range(evidence.report['steps']):
            if perf_counter()-started > evidence.report['maximum_wall_seconds']:
                raise RuntimeError('Safe-save wall boundary; accepted states preserved.')
            values = exponential_midpoint(split, values, step,
                first_remainder=encoded_flow if index == 0 else None)
            state = split.physical(values)
            if not np.all(np.isfinite(state)):
                raise RuntimeError('Nonfinite time64 state.')
            path = evidence.output/('steps64-accepted'+str(index+1).zfill(3)+'.npz')
            np.savez_compressed(path, time=(index+1)*step, state=state, modal_increment=values)
            evidence.own(path, 'outputs')
            states.append(state.copy())
            evidence.report.update(accepted=index+1, accepted_time=(index+1)*step,
                evaluations=split.evaluations, seconds=perf_counter()-started)
            evidence.save()
            if (index+1) % 8 == 0:
                print(json.dumps(dict(branch=args.branch, accepted=index+1,
                    total=64, seconds=perf_counter()-started)), flush=True)
        trajectory_path = evidence.output/'trajectory-steps64.npz'
        np.savez_compressed(trajectory_path, times=np.linspace(0.,4e-5,65),
            states=np.asarray(states), final_modal_increment=values)
        evidence.own(trajectory_path, 'outputs')
        evidence.save()
        tangent, diagnostic = force_data(system, state)
        lapse, root = tangent.geometry.metric(state[0, :, -1])
        timelike = float(np.max(abs(tangent.rates[:, -1]/(lapse*root))))
        minimum_jacobian = float(tangent.material.minimum_jacobian)
        force = diagnostic['lift']['force']
        evidence.check('final_constraints', diagnostic['canonical'] < 2e-11
            and max(diagnostic['radial']) < 2e-9, dict(canonical=diagnostic['canonical'], radial=diagnostic['radial']))
        evidence.check('final_force_identity', diagnostic['lift']['identity_error'] < 2e-9
            and diagnostic['schur']['force_identity_error'] < 2e-9)
        evidence.check('final_current_Euler', diagnostic['noether']['residual'] < 2e-9
            and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
        evidence.check('final_regular_domain', minimum_jacobian > 0 and timelike < 1,
            dict(minimum_jacobian=minimum_jacobian, maximum_timelike_speed=timelike))
        previous_encoded = split.encode(old['state']-initial)
        current_encoded = split.encode(state-initial)
        force_change = force-old_case['force']
        row = dict(branch=args.branch, steps=64, previous_steps=32, fine_steps=fine_steps,
            old_coarse_force=old_case['force'], new_coarse_force=force, fine_force=fine_case['force'],
            continuum_force=old_status['continuum_force'], signed_coarse_time_force_change=force_change,
            absolute_coarse_time_force_change=abs(force_change),
            old_coarse_fine_force_difference=fine_case['force']-old_case['force'],
            new_coarse_fine_force_difference=fine_case['force']-force,
            old_coarse_fine_relative_force_difference=abs(fine_case['force']-old_case['force'])/abs(fine_case['force']),
            new_coarse_fine_relative_force_difference=abs(fine_case['force']-force)/abs(fine_case['force']),
            new_coarse_continuum_relative_force_error=abs(force-old_status['continuum_force'])/abs(old_status['continuum_force']),
            fixed_fine_continuum_relative_force_error=abs(fine_case['force']-old_status['continuum_force'])/abs(old_status['continuum_force']),
            relative_canonical_state_change=split.relative_energy_difference(previous_encoded, current_encoded),
            maximum_rotation_angle=float(step*np.max(split.frequency)),
            minimum_material_jacobian=minimum_jacobian, maximum_timelike_speed=timelike,
            valid_for_claim=False)
        evidence.report['cases'].append(row)
        evidence.report['endpoint_diagnostic'] = diagnostic
        evidence.report.update(seconds=perf_counter()-started,
            force_improvement_is_observed_not_acceptance_gate=True,
            impulse_not_recomputed=True, previous_long_window_not_retested=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']),
            seconds=perf_counter()-started, **row)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
