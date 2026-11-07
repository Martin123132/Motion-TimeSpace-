from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_position_reaction_20260929 import ResponseSum, native_position_force
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-native-position-label-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+1500
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False,
            numerical_acceptance_passed=False, scope='Refine the MTS-fine native position-force label rule only',
            full_live_sensitivity_recomputed=False, original_reaction_replaced=False,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root/'DERIVATION-20260929-native-position-force-label-resolution.md')
        parent_path = evidence.output.parent/'annular-position-reaction-diagnostic-attempt03/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('MTS_fine_parent_complete', parent['state'] == 'complete' and parent['diagnostic_only'])
        digests = dict(parent['inputs'], **parent['outputs'])

        def owned(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if hashlib.sha256(path.read_bytes()).hexdigest() != digests[key]:
                raise RuntimeError('Changed native refinement input: '+key)
            evidence.own(path)
            return path

        def read(relative):
            path = owned(relative)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        status = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
        match = lambda report: next(row for row in report['cases'] if row['branch'] == 'MTS-primary' and row['level'] == 'fine')
        loads, action, sources = restore_case(evidence, digests, 'MTS-primary', 'fine', deadline)
        for relative in sources.values():
            owned(relative)
        live = match(status('annular-live-support-acceleration-attempt01'))
        positions = match(status('annular-compensated-position-attempt04'))
        jets = match(status('annular-position-metric-jet-validation-attempt01'))
        directions = read(live['direction_path'])
        correction = read(live['paths']['projection'])['correction']

        def response(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        position = ResponseSum(response(read(positions['paths']['response'])),
            response(read(jets['paths']['transported_old_metric'])))
        packet = read(sources['packet'])
        native = NativeKernel(action.mesh, packet['gram_support'], True)
        owner = read(sources['parent'])
        centre = next(row for row in owner['centres'] if row.get('route') == 'resampled')
        inverse = BandedSourceInverse(load_npz(owned(centre['matrix_path'])), loads.rates.shape)
        norm = lambda value: float(np.max(np.abs(inverse.solve(value.ravel()))))
        saved = read(match(parent)['paths']['material64'])
        baseline, previous = saved['force_native'], saved['force_native']
        field_direction = directions['field_vertices']-correction[:, :-1]
        source_direction = -correction[:, -1]
        rows = []
        with localcontext() as context:
            context.prec = 70
            for order in [96, 128, 256]:
                points, weights = np.polynomial.legendre.leggauss(order)
                labels, weights = points/2, weights/2
                weights *= 6*(labels+.5)*(.5-labels)
                force, halving, base = [np.zeros_like(loads.rates) for unused in range(3)]
                for index, (label, weight) in enumerate(zip(labels, weights)):
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe native-force label-refinement boundary')
                    cardinal = np.asarray(action.cardinal(label)).ravel()
                    value, difference, original = native_position_force(native, loads, action, label,
                        field_direction, source_direction, directions['edge_vertices'], position)
                    force += weight*np.outer(cardinal, value)
                    halving += weight*np.outer(cardinal, difference)
                    base += weight*np.outer(cardinal, original)
                    if index % 16 == 15:
                        evidence.report['progress'] = dict(stage='native'+str(order)+':'+str(index+1), seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']), flush=True)
                evidence.check('finite_native_rule_'+str(order), np.all(np.isfinite(force)))
                evidence.check('native_derivative_step_halving_'+str(order), norm(halving) <= 2e-11, norm(halving))
                successive = norm(force-previous)
                row = dict(material_order=order, maximum_force=float(np.max(np.abs(force))),
                    difference_from_64_inverse=norm(force-baseline), successive_inverse=successive,
                    successive_within_2e11=successive <= 2e-11, derivative_halving_inverse=norm(halving),
                    seconds=perf_counter()-started, valid_for_claim=False)
                path = evidence.output/('native-position-force-'+str(order)+'.npz')
                np.savez_compressed(path, force_native=force, native_halving_difference=halving, base_force_native=base)
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                rows.append(row)
                previous = force
                evidence.save()
                print(json.dumps(row), flush=True)
        path = evidence.output/'native-label-resolution.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
