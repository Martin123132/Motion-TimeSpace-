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
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-bulk513-MTS-time128-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch='MTS',
            full_live_P2_force_convergence_proven=False, base_count=513, source_cap=1e-5,
            duration=4e-5, steps=128, maximum_wall_seconds=6000.,
            previous_point004_window_not_retested=True, all_modes_and_Gram_retained=True,
            initial_preparation_unchanged=True, time_force_budget=2e-9, time_state_budget=1e-6,
            endpoint_force_threshold=2.700598122731542e-8,
            further_time_refinement_not_independent_time_integrator=True)
        prior_folder = 'annular-P2-bulk513-evolution-MTS-attempt01'
        prior_path = evidence.output.parent/prior_folder/'status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        old = checked_load(evidence, prior_folder, 'trajectory-steps64.npz')
        initial = old['states'][0]
        system = IndexedGradedP2System(513, True, 1e-5)
        rates, geometry = system.solve(*initial)
        split = FrozenCanonicalSplit(system, initial, geometry)
        split.started, split.maximum_wall_seconds = started, evidence.report['maximum_wall_seconds']
        evidence.check('all_fine_modes_and_basis_qualified', np.all(split.frequency[:, :-1] > 0)
            and max(row['mass_orthogonality'] for row in split.factor_diagnostics) < 2e-12
            and max(row['normwise_backward_residual'] for row in split.factor_diagnostics) < 2e-11)
        first = split.encode(np.stack([rates, system.forces(initial[0], rates, geometry)]))
        values = np.zeros_like(initial)
        states = [initial.copy()]
        step = evidence.report['duration']/128
        for index in range(128):
            values = exponential_midpoint(split, values, step, first_remainder=first if index == 0 else None)
            state = split.physical(values)
            if not np.all(np.isfinite(state)):
                raise RuntimeError('Nonfinite further-refined state.')
            states.append(state.copy())
            path = evidence.output/('steps128-accepted'+str(index+1).zfill(3)+'.npz')
            np.savez_compressed(path, time=(index+1)*step, state=state, modal_increment=values)
            evidence.own(path, 'outputs')
            evidence.report.update(accepted=index+1, accepted_time=(index+1)*step, seconds=perf_counter()-started)
            evidence.save()
            if (index+1) % 16 == 0:
                print(json.dumps(dict(accepted=index+1, seconds=perf_counter()-started)), flush=True)
        tangent, diagnostic = force_data(system, state)
        oracle_data = checked_load(evidence, 'annular-P2-live-exponential-short-continuum-attempt01', 'continuum512.npz')
        oracle = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        unused, target, forces = oracle.rhs_with_geometry(oracle_data['state'])
        target_force = float(forces['radiation'][4])
        comparison = physical_comparison(system, state[0], tangent.rates, tangent.geometry, oracle, target)
        current = tangent.layer_data(0.)
        mass, unused = scalar_pencil(current.layer, current.coordinates)
        gram = gram_jump_split(current.layer, current.coordinates, mass)
        force = diagnostic['lift']['force']
        force_error = abs(force-target_force)
        time_force = abs(force-prior['refined_force'])
        time_state = split.relative_energy_difference(values, old['final_modal_increment'])
        row = dict(steps=128, force=force, force_error=force_error,
            instantaneous_relative_force_error=force_error/abs(target_force),
            gram_split=gram, maximum_rotation_angle=float(step*np.max(split.frequency)), **diagnostic, **comparison)
        evidence.report['cases'].append(row)
        evidence.check('endpoint_constraints_and_current', diagnostic['canonical'] < 2e-11
            and max(diagnostic['radial']) < 2e-9 and diagnostic['noether']['residual'] < 2e-9
            and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
        evidence.check('endpoint_force_identities', diagnostic['lift']['identity_error'] < 2e-9
            and diagnostic['schur']['force_identity_error'] < 2e-9)
        lapse, root = tangent.geometry.metric(state[0, :, -1])
        evidence.check('regular_domain', tangent.material.minimum_jacobian > 0
            and np.max(abs(tangent.rates[:, -1]/(lapse*root))) < 1)
        path = evidence.output/'trajectory-steps128.npz'
        np.savez_compressed(path, times=np.linspace(0., evidence.report['duration'], 129), states=np.array(states),
            final_modal_increment=values)
        evidence.own(path, 'outputs')
        time_pass = time_force < 2e-9 and time_state < 1e-6
        endpoint_pass = (time_pass and force_error <= evidence.report['endpoint_force_threshold']
            and comparison['field_error'] < .005 and comparison['source_error'] < 5e-7
            and comparison['velocity_error'] < 2e-5 and comparison['clock_rate_error'] < 2e-7)
        evidence.report.update(continuum_force=target_force, refined_force=force, refined_force_error=force_error,
            previous_64_force=prior['refined_force'], previous_32_to_64_force_change=prior['time_force_difference'],
            time_force_difference=time_force, time_state_difference=time_state,
            empirical_time_budget_pass=bool(time_pass), scoped_endpoint_gate_pass=bool(endpoint_pass),
            force_difference_ratio=prior['time_force_difference']/max(time_force, 1e-300),
            force_error_ratio_to_coarse_space=force_error/prior['baseline_force_error'], seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', force=force, force_error=force_error, time_force=time_force,
            ratio=evidence.report['force_difference_ratio'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
