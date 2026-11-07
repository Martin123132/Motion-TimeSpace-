from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_high_order_native_v2_20261003 import adapt_owner, HighLoads, HighAction, HighInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from analyze_annular_source_flat_state_20261002 import read_archive
from annular_balanced_native_force_20261003 import balanced_field_force
from construct_annular_septic_response_20261003 import pin
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import argparse
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['primary', 'reference'], required=True)
    parser.add_argument('--cpu', type=int, required=True)
    args = parser.parse_args()
    pin(args.cpu)
    evidence = EvidenceRun('annular-balanced-force-' + args.branch + '-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 5400
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-all-native-jump-live-' + args.branch + '-attempt01/status.json')
        mesh = json.loads((evidence.root / parent['mesh_path']).read_text())
        saved = read_archive(evidence.root / parent['states'][0]['path'])
        seal = evidence.output.parent / 'annular-septic-coupled-response-integrity-20261003.json'
        evidence.own(seal)
        evidence.report.update(results=[], states=parent['states'], mesh_path=parent['mesh_path'], branch=args.branch,
            same_initial_profile=True, same_own_metric=True, same_full_Hessian=True, alternate_equivalent_force_assembly=True,
            github_action=False, subagents_used=False)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
        with localcontext() as context:
            context.prec = 75
            unused, original, sources = restore_case(evidence, json.loads(seal.read_text())['hashes'], 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            loads = HighLoads(owner, decimals(saved['coordinates']), saved['rates'], mesh, args.branch, deadline)
            solver, solution = reconstructed_solver(saved)
            action = HighAction(loads, mesh, solver, solution)
        accelerations = []
        for row in parent['results']:
            data = read_archive(evidence.root / row['path'])
            matrix = load_npz(evidence.root / row['matrix_path'])
            inverse = HighInverse(matrix, data['acceleration'].shape, 7)
            balanced = balanced_field_force(loads, action, row['spatial'], row['material'], deadline, progress)
            force = data['force'].copy()
            force[:, :-1] = balanced['force']
            force_difference = float(np.max(abs(force - data['force'])))
            relative_force = force_difference / float(np.max(abs(data['force'])))
            evidence.check(row['name'] + ':weak_and_integrated_force_consistency', relative_force < 2e-10, relative_force)
            acceleration = inverse.solve(force.ravel()).reshape(force.shape)
            for repeat in range(2):
                residual = (matrix @ acceleration.ravel()).reshape(force.shape) - force
                acceleration -= inverse.solve(residual.ravel()).reshape(force.shape)
            residual = (matrix @ acceleration.ravel()).reshape(force.shape) - force
            euler = inverse.residual_norm(residual) / inverse.residual_norm(force)
            evidence.check(row['name'] + ':balanced_Euler', euler < 2e-11, euler)
            cardinal = np.array([np.asarray(action.cardinal(label)).ravel() for label in data['labels']])
            source_acceleration = cardinal @ acceleration[:, -1]
            trace = data['speed_square'][:, None] * data['curvatures'] + (data['drift'] + source_acceleration)[:, None] * data['slopes']
            corner = data['native_speed_square'] * data['native_curvature_jumps']
            corner += (data['native_drift'] + data['native_displacement'] * source_acceleration[:, None]) * data['native_slope_jumps']
            changed = dict(data, acceleration=acceleration, force=force, residual=residual,
                wave_source_force=force - data['native_force'], source_acceleration=source_acceleration, trace=trace, native_corner=corner,
                original_acceleration=data['acceleration'], original_force=data['force'], balanced_bulk=balanced['bulk'], balanced_traction=balanced['traction'])
            path = evidence.output / (row['name'] + '-acceleration.npz')
            np.savez_compressed(path, **changed)
            evidence.own(path, 'outputs')
            item = dict(row, path=str(path.relative_to(evidence.root)), Euler_relative=float(euler),
                maximum_trace_residual=float(np.max(abs(trace))), maximum_native_curvature_corner=float(np.max(abs(corner))),
                maximum_acceleration=float(np.max(abs(acceleration))), force_form_absolute_difference=force_difference,
                force_form_relative_difference=relative_force, acceleration_form_difference=float(np.max(abs(acceleration - data['acceleration']))))
            item['initial_gates'] = dict(row['initial_gates'], source=item['maximum_trace_residual'] < 1e-9,
                native_curvature=item['maximum_native_curvature_corner'] < 1e-9)
            item['initial_candidate'] = args.branch == 'primary' and all(item['initial_gates'].values())
            evidence.report['results'].append(item)
            accelerations.append(acceleration)
            evidence.save()
        evidence.report.update(initial_candidate=all(row['initial_candidate'] for row in evidence.report['results']),
            quadrature_acceleration_difference=float(np.max(abs(accelerations[1] - accelerations[0]))),
            seconds=perf_counter() - started, time_response_not_yet_checked=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
