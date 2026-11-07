from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_high_order_native_v2_20261003 import adapt_owner, HighInverse
from annular_product_live_20261003 import live_product
from annular_balanced_native_force_20261003 import balanced_field_force
from scipy.sparse import load_npz
from annular_high_order_coupled_v2_20261003 import coupled_high
from annular_candidate_hamiltonian_20260921 import decimals
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from construct_annular_septic_response_20261003 import pin
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
    evidence = EvidenceRun('annular-product-basis-live-' + args.branch + '-attempt02', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-all-native-jump-response.md')
        diagnostic = verify_report(evidence, 'source-intake/navier-stokes/20260914/annular-force-basis-diagnostic-' + args.branch + '-attempt01/status.json')
        evidence.check('selected_product_force_oracle', all(row['original_equivalence_gate_passed'] for row in diagnostic['results']))
        prepared = verify_report(evidence, 'source-intake/navier-stokes/20260914/annular-all-native-jump-construction-attempt02/status.json')
        evidence.check('construction_complete', prepared['state'] == 'complete')
        mesh = json.loads((evidence.root / prepared['mesh_path']).read_text())
        saved = read_archive(evidence.root / prepared['initial_path'])
        coordinates, rates = decimals(saved['coordinates']), saved['rates']
        seal = evidence.output.parent / 'annular-septic-coupled-response-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        evidence.report.update(results=[], balanced_results=[], states=[], mesh_path=prepared['mesh_path'], branch=args.branch,
            source_acceleration_fitted=False, physical_evolution=False, github_action=False, subagents_used=False,
            cpu=args.cpu, same_initial_profile=True, native_support_unchanged=True, degree=7)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe septic stage boundary')
        with localcontext() as context:
            context.prec = 64
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(original.owner, mesh)
            progress('own septic radial gravity')
            loads, action = live_product(owner, coordinates, rates, mesh, args.branch, deadline)
        radial = float(np.max(abs(action.solver.residual(action.solution['state'], args.branch))))
        evidence.check('own_radial_constraint', radial < 8e-14, radial)
        path = evidence.output / 'P7-live-state.npz'
        np.savez_compressed(path, coordinates=np.asarray(coordinates, str), rates=rates, edges=action.solver.edges, **action.solution)
        evidence.own(path, 'outputs')
        evidence.report['states'].append(dict(name='P7', path=str(path.relative_to(evidence.root))))
        outputs = []
        for spatial, material in [(12, 48), (16, 64)]:
            arrays, row = coupled_high(evidence, loads, action, args.branch, args.branch + '-' + str(spatial) + '-' + str(material),
                spatial, material, deadline, progress)
            arrays = {key: np.asarray(value) for key, value in arrays.items()}
            outputs.append(arrays)
            balanced = balanced_field_force(loads, action, spatial, material, deadline, progress)
            force = arrays['force'].copy()
            force[:, :-1] = balanced['force']
            force_error = float(np.max(abs(force - arrays['force'])) / np.max(abs(arrays['force'])))
            evidence.check(row['name'] + ':product_and_integrated_force', force_error < 2e-10, force_error)
            matrix = load_npz(evidence.root / row['matrix_path'])
            inverse = HighInverse(matrix, arrays['acceleration'].shape, 7)
            acceleration = inverse.solve(force.ravel()).reshape(force.shape)
            for repeat in range(2):
                residual = (matrix @ acceleration.ravel()).reshape(force.shape) - force
                acceleration -= inverse.solve(residual.ravel()).reshape(force.shape)
            residual = (matrix @ acceleration.ravel()).reshape(force.shape) - force
            euler = inverse.residual_norm(residual) / inverse.residual_norm(force)
            evidence.check(row['name'] + ':balanced_Euler', euler < 2e-11, float(euler))
            cardinal = np.array([np.asarray(action.cardinal(label)).ravel() for label in arrays['labels']])
            source_acceleration = cardinal @ acceleration[:, -1]
            trace = arrays['speed_square'][:, None] * arrays['curvatures'] + (arrays['drift'] + source_acceleration)[:, None] * arrays['slopes']
            corner = arrays['native_speed_square'] * arrays['native_curvature_jumps']
            corner += (arrays['native_drift'] + arrays['native_displacement'] * source_acceleration[:, None]) * arrays['native_slope_jumps']
            changed = dict(arrays, acceleration=acceleration, force=force, residual=residual,
                wave_source_force=force-arrays['native_force'], source_acceleration=source_acceleration, trace=trace, native_corner=corner,
                product_acceleration=arrays['acceleration'], product_force=arrays['force'])
            path = evidence.output / (row['name'] + '-balanced-acceleration.npz')
            np.savez_compressed(path, **changed)
            evidence.own(path, 'outputs')
            item = dict(row, path=str(path.relative_to(evidence.root)), Euler_relative=float(euler),
                maximum_trace_residual=float(np.max(abs(trace))), maximum_native_curvature_corner=float(np.max(abs(corner))),
                maximum_acceleration=float(np.max(abs(acceleration))), force_form_relative_difference=force_error,
                acceleration_form_difference=float(np.max(abs(acceleration-arrays['acceleration']))))
            item['initial_gates'] = dict(row['initial_gates'], source=item['maximum_trace_residual'] < 1e-9,
                native_curvature=item['maximum_native_curvature_corner'] < 1e-9)
            item['initial_candidate'] = args.branch == 'primary' and all(item['initial_gates'].values())
            evidence.report['balanced_results'].append(item)
            evidence.save()
        evidence.report.update(seconds=perf_counter() - started, own_metric_solved=True, full_acceleration_solved=True,
            quadrature_acceleration_difference=float(np.max(abs(outputs[1]['acceleration'] - outputs[0]['acceleration']))),
            quadrature_source_acceleration_difference=float(np.max(abs(outputs[1]['acceleration'][:, -1] - outputs[0]['acceleration'][:, -1]))),
            initial_candidate=all(row['initial_candidate'] for row in evidence.report['results']),
            continuous_material_bound_proven=False, spatial_refinement_done_for_this_state=False, second_order_preservation_done=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()




