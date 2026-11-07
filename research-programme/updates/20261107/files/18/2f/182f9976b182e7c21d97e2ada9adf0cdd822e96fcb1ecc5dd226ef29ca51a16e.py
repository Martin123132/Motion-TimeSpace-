from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_high_order_native_v2_20261003 import adapt_owner, live_high
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
    evidence = EvidenceRun('annular-all-native-jump-live-' + args.branch + '-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-all-native-jump-response.md')
        prepared = verify_report(evidence, 'source-intake/navier-stokes/20260914/annular-all-native-jump-construction-attempt02/status.json')
        evidence.check('construction_complete', prepared['state'] == 'complete')
        mesh = json.loads((evidence.root / prepared['mesh_path']).read_text())
        saved = read_archive(evidence.root / prepared['initial_path'])
        coordinates, rates = decimals(saved['coordinates']), saved['rates']
        seal = evidence.output.parent / 'annular-septic-coupled-response-integrity-20261003.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        evidence.report.update(results=[], states=[], mesh_path=prepared['mesh_path'], branch=args.branch,
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
            loads, action = live_high(owner, coordinates, rates, mesh, args.branch, deadline)
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
            outputs.append(arrays)
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
