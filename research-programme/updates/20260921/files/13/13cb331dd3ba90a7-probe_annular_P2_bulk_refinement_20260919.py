from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_bulk_refinement_20260919 import indexed_initial, gram_jump_split
from annular_P2_graded_source_20260919 import scalar_pencil, frequency_diagnostic
from annular_live_P2_current_20260918 import LiveP2Tangent
from run_annular_P2_evolved_source_halving_20260919 import force_data
from run_annular_P2_continuum_bridge_20260918 import checked_load
from budget_annular_P2_saved_force_20260918 import checked_json
from time import perf_counter
import argparse
import contextlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['reference', 'MTS'], required=True)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-P2-bulk513-preflight-'+args.branch+'-attempt01', __file__)
    try:
        started = perf_counter()
        evidence.report.update(github_action=False, subagents_used=False, branch=args.branch,
            full_live_P2_force_convergence_proven=False, base_count=513, source_cap=1e-5,
            no_forward_evolution=True, analytic_preparation_unchanged=True,
            full_Gram_retained=True, spatial_sequence_not_exact_same_finite_Gram_matrix=True,
            planned_duration=4e-5, planned_time_steps=[32, 64],
            maximum_forward_wall_seconds=6000., initial_force_threshold=2.700598122731542e-8)
        prerequisite = evidence.output.parent/'annular-P2-live-exponential-final-integrity.json'
        status = json.loads(prerequisite.read_text())
        evidence.own(prerequisite)
        evidence.check('previous_checkpoint_complete', status['state'] == 'complete'
            and all(row['passed'] for row in status['checks']))
        coarse = IndexedGradedP2System(257, args.branch == 'MTS', 2e-5)
        saved = checked_load(evidence, 'annular-P2-joint-refinement-257-cap2e-05-attempt01', args.branch+'-initial.npz')
        coordinates, momenta, prepared, geometry = indexed_initial(coarse)
        errors = dict(coordinates=float(np.max(abs(coordinates-saved['coordinates']))),
            momenta=float(np.max(abs(momenta-saved['momenta']))),
            rates=float(np.max(abs(prepared-saved['rates']))))
        evidence.check('indexed_preparation_matches_original_saved_preparation',
            errors['coordinates'] == 0 and errors['momenta'] < 2e-12 and errors['rates'] < 2e-11, errors)
        evidence.report['preparation_control'] = errors
        coarse_layer = coarse.layer(0., geometry)
        coarse_central = coordinates[len(coarse.labels)//2]
        coarse_mass, unused = scalar_pencil(coarse_layer, coarse_central)
        coarse_split = gram_jump_split(coarse_layer, coarse_central, coarse_mass)
        system = IndexedGradedP2System(513, args.branch == 'MTS', 1e-5)
        coordinates, momenta, prepared, geometry = indexed_initial(system)
        initial = np.stack([coordinates, momenta])
        path = evidence.output/'initial.npz'
        np.savez_compressed(path, coordinates=coordinates, momenta=momenta, prepared_rates=prepared,
            labels=system.labels)
        evidence.own(path, 'outputs')
        rhs_started = perf_counter()
        flow = system.rhs(0., initial.ravel()).reshape(initial.shape)
        rhs_seconds = perf_counter()-rhs_started
        evidence.check('finite_prepared_RHS', np.all(np.isfinite(flow))
            and np.max(abs(flow[0]-prepared)) < 2e-11)
        tangent, diagnostic = force_data(system, initial)
        layer = tangent.layer_data(0.).layer
        central = tangent.layer_data(0.).coordinates
        mass, unused = scalar_pencil(layer, central)
        split = gram_jump_split(layer, central, mass)
        spectrum = frequency_diagnostic(layer, central)
        probe = central.copy()
        probe[:-1] = .001*np.sin(3.7*layer.radii)+.0002*np.cos(8.2*layer.radii)
        arbitrary_split = gram_jump_split(layer, probe, mass)
        for tag, row in [('initial', split), ('arbitrary', arbitrary_split)]:
            evidence.check(tag+'_Gram_expansion', row['factor_identity_error'] < 2e-11
                and row['action_identity_error'] < 2e-10*max(1., row['action_scale'])
                and row['energy_identity_error'] < 2e-11*max(1., abs(row['gram_energy'])))
        evidence.check('positive_and_consistent_frozen_spectrum', spectrum['minimum_eigenvalue'] > 0
            and spectrum['stiffness_action_error'] < 2e-8)
        evidence.check('initial_constraints_and_force_identities', diagnostic['canonical'] < 2e-11
            and max(diagnostic['radial']) < 2e-9 and diagnostic['lift']['identity_error'] < 2e-9
            and diagnostic['schur']['force_identity_error'] < 2e-9)
        evidence.check('initial_current_Euler', diagnostic['noether']['residual'] < 2e-9
            and diagnostic['noether']['source_euler'] < 2e-8 and diagnostic['noether']['scalar_euler'] < 2e-8)
        maximum_ratio = float(np.max(abs(tangent.rates[:, -1]/np.prod(
            tangent.geometry.metric(coordinates[:, -1]), axis=0))))
        evidence.check('regular_material_timelike_domain', tangent.material.minimum_jacobian > 0 and maximum_ratio < 1)
        predicted_evolution = 2*sum(evidence.report['planned_time_steps'])*rhs_seconds
        force = diagnostic['lift']['force']
        comparison = checked_json(evidence, 'annular-P2-continuum-comparison-65-attempt01', args.branch+'-65.json')
        target_force = comparison['times'][0]['continuum_wave_force']
        initial_gate = abs(force-target_force) <= evidence.report['initial_force_threshold']
        time_step = evidence.report['planned_duration']/evidence.report['planned_time_steps'][-1]
        evidence.report.update(scalar_nodes=system.count, labels=len(system.labels),
            initial_force=force, continuum_initial_force=target_force, initial_force_gate_pass=bool(initial_gate),
            diagnostic=diagnostic, gram_split=split, arbitrary_gram_split=arbitrary_split,
            coarse_initial_gram_split=coarse_split,
            spectral=spectrum, rhs_seconds=rhs_seconds,
            predicted_evolution_seconds=predicted_evolution,
            cost_estimate_not_runtime_guarantee=True, fine_frozen_rotation_angle=time_step*spectrum['maximum_angular_frequency'],
            forward_candidate_allowed=bool(initial_gate and predicted_evolution < 4500.),
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps({name:evidence.report[name] for name in ['state', 'branch', 'scalar_nodes',
            'initial_force', 'initial_force_gate_pass', 'rhs_seconds', 'predicted_evolution_seconds',
            'fine_frozen_rotation_angle', 'forward_candidate_allowed', 'seconds']}), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
