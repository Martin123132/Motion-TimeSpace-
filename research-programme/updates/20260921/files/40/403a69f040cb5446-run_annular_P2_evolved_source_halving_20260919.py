from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_graded_source_20260919 import GradedP2System, force_schur_identity
from annular_P2_live_exponential_20260919 import FrozenCanonicalSplit, exponential_midpoint
from annular_live_P2_current_20260918 import LiveP2Tangent
from derive_annular_P2_conforming_force_lift_20260918 import conforming_force_lift
from annular_live_barycentric_20260915 import BarycentricLiveContinuum
from compare_annular_P2_continuum_bridge_20260918 import physical_comparison
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def force_data(system, state):
    tangent = LiveP2Tangent(system, *state)
    lifted = conforming_force_lift(tangent)
    schur = force_schur_identity(tangent.layer_data(0.))
    return tangent, dict(lift=lifted, schur=schur,
        canonical=system.canonical_residual(*state, tangent.rates, tangent.geometry),
        radial=list(tangent.geometry.off_grid_residual(tangent.rates)),
        noether=tangent.layer_data(0.).noether())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-evolved-source-halving-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, source_cap=2e-5, base_count=257,
            duration=4e-5, steps=[16, 32], maximum_wall_seconds=1500.,
            source_refinement_only_not_joint_spatial_convergence=True,
            old_point004_window_not_retested=True, initial_preparation_unchanged=True,
            modes_Gram_and_force_unchanged=True, time_force_budget=2e-9, time_state_budget=1e-6)
        control_folder = 'annular-P2-indexed-full-pilot-control-'+args.branch+'-attempt01'
        control_path = evidence.output.parent/control_folder/'status.json'
        control = json.loads(control_path.read_text())
        evidence.own(control_path)
        evidence.check('prior_independent_whole_pilot_control_qualified', control['state'] == 'complete'
            and control['independent_short_pilot_agreement_pass'])
        baseline = checked_load(evidence, control_folder, 'tight-trajectory.npz')
        baseline_system = IndexedGradedP2System(257, args.branch == 'MTS', 4e-5)
        baseline_tangent, baseline_diagnostic = force_data(baseline_system, baseline['states'][-1])
        evidence.check('baseline_RK_force_reproduced', abs(baseline_diagnostic['lift']['force']
            -control['cases'][-1]['endpoint']['reduced_wave_force']) < 2e-10)
        oracle_saved = checked_load(evidence, 'annular-P2-live-exponential-short-continuum-attempt01', 'continuum512.npz')
        oracle = BarycentricLiveContinuum(512, 8, 18, radial_spacing=.025, label_order=12)
        unused, target, forces = oracle.rhs_with_geometry(oracle_saved['state'])
        oracle_force = float(forces['radiation'][4])
        data = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', args.branch+'-initial.npz')
        initial = np.stack([data['coordinates'], data['momenta']])
        system = IndexedGradedP2System(257, args.branch == 'MTS', 2e-5)
        original = GradedP2System(257, args.branch == 'MTS', 2e-5)
        old_flow = original.rhs(0., initial.ravel())
        rates, geometry = system.solve(*initial)
        flow = np.stack([rates, system.forces(initial[0], rates, geometry)]).ravel()
        error = float(np.max(abs(flow-old_flow)))
        evidence.check('halved_source_grid_indexed_original_RHS_matches', error < 2e-9, error)
        split = FrozenCanonicalSplit(system, initial, geometry)
        split.started, split.maximum_wall_seconds = started, evidence.report['maximum_wall_seconds']
        evidence.check('halved_source_all_modes_positive_retained', system.count == 558
            and split.frequency.shape == (15, 559) and np.all(split.frequency[:, :-1] > 0))
        evidence.report['factor_diagnostics'] = split.factor_diagnostics
        first_remainder = split.encode(flow.reshape(initial.shape))
        zero = np.zeros_like(initial)
        endpoints = []
        for steps in evidence.report['steps']:
            values = zero.copy()
            step = evidence.report['duration']/steps
            for index in range(steps):
                values = exponential_midpoint(split, values, step,
                    first_remainder=first_remainder if index == 0 else None)
                if not np.all(np.isfinite(values)):
                    raise RuntimeError('Nonfinite source-refined state.')
                state = split.physical(values)
                path = evidence.output/('steps'+str(steps)+'-accepted'+str(index+1).zfill(3)+'.npz')
                np.savez_compressed(path, time=(index+1)*step, state=state, modal_increment=values)
                evidence.own(path, 'outputs')
                evidence.report.update(active_steps=steps, accepted=index+1, accepted_time=(index+1)*step,
                    evaluations=split.evaluations, seconds=perf_counter()-started)
                evidence.save()
            tangent, diagnostic = force_data(system, state)
            comparison = physical_comparison(system, state[0], tangent.rates, tangent.geometry, oracle, target)
            force = diagnostic['lift']['force']
            force_error = abs(force-oracle_force)
            row = dict(steps=steps, force=force, force_error=force_error,
                instantaneous_force_relative_error=force_error/abs(oracle_force),
                peak_scaled_force_gate_pass=bool(force_error <= 2.700598122731542e-8),
                maximum_rotation_angle=float(step*np.max(split.frequency)), **comparison, **diagnostic)
            evidence.report['cases'].append(row)
            evidence.save()
            evidence.check('steps'+str(steps)+'_constraints', diagnostic['canonical'] < 2e-11
                and max(diagnostic['radial']) < 2e-9)
            evidence.check('steps'+str(steps)+'_force_identity', diagnostic['lift']['identity_error'] < 2e-9
                and diagnostic['schur']['force_identity_error'] < 2e-9)
            evidence.check('steps'+str(steps)+'_current_Euler', diagnostic['noether']['residual'] < 2e-9
                and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
            endpoints.append(values.copy())
            print(json.dumps(dict(branch=args.branch, steps=steps, force=force,
                force_error=force_error, seconds=perf_counter()-started)), flush=True)
        time_force = abs(evidence.report['cases'][0]['force']-evidence.report['cases'][1]['force'])
        time_state = split.relative_energy_difference(*endpoints)
        baseline_force = baseline_diagnostic['lift']['force']
        final = evidence.report['cases'][-1]
        material_pass = final['source_error'] < 5e-7 and final['velocity_error'] < 2e-5 and final['clock_rate_error'] < 2e-7
        time_pass = time_force < evidence.report['time_force_budget'] and time_state < evidence.report['time_state_budget']
        evidence.report.update(baseline_force=baseline_force, baseline_force_error=abs(baseline_force-oracle_force),
            baseline_force_decomposition=baseline_diagnostic, continuum_force=oracle_force,
            refined_force=final['force'], refined_force_error=final['force_error'],
            force_error_ratio_refined_to_baseline=final['force_error']/max(abs(baseline_force-oracle_force), 1e-300),
            time_force_difference=time_force, time_state_difference=time_state, empirical_time_budget_pass=bool(time_pass),
            scoped_endpoint_gate_pass=bool(time_pass and material_pass and final['peak_scaled_force_gate_pass']
                and final['field_error'] < .005), valid_for_physics_claim=False, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(branch=args.branch, state='complete', refined_force=final['force'],
            ratio=evidence.report['force_error_ratio_refined_to_baseline'], time_pass=bool(time_pass),
            endpoint_pass=evidence.report['scoped_endpoint_gate_pass'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
