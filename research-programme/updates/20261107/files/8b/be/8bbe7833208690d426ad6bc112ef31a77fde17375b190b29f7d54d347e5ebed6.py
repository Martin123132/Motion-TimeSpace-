from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from validate_annular_reacted_column_sensitivity_20260929 import acceleration_channels
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from decimal import localcontext
from time import perf_counter
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-C2-cancellation-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1200
    try:
        parent_path = evidence.output.parent / 'annular-reacted-support-columns-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = {}
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = evidence.root / relative
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed input: ' + relative)
                digests[str(path.relative_to(evidence.root))] = expected
                evidence.own(path)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        live = read(str((evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json').relative_to(evidence.root)))
        case = next(row for row in live['cases'] if row['branch'] == 'reference-reference' and row['level'] == 'third')
        with localcontext() as context:
            context.prec = 70
            loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
            directions = read(case['direction_path'])
            correction = read(case['paths']['projection'])['correction']
            archive = read(case['paths']['live_response'])
            solver, solution = reconstructed_solver(archive)
            response = MetricResponse(solver, solution, archive['forcing'], 0., [])
            acceleration = np.column_stack([directions['field_vertices'] - correction[:, :-1], -correction[:, -1]])
            result = acceleration_channels(action, loads, directions, acceleration, response, 1., 64, deadline)
            path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/live-acceleration-current-moments.csv'
            with path.open(newline='', encoding='utf-8') as handle:
                rows = list(csv.DictReader(handle))
            inherited = np.r_[case['summary']['live_projected_coefficient'],
                [float(next(row for row in rows if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['power']) == power)['total']) for power in range(3)]]
            error = abs(result - inherited)
            evidence.check('unchanged_C2_replay_gate', np.all(error <= 2e-24 + 2e-6 * abs(inherited)),
                dict(result=result.tolist(), inherited=inherited.tolist(), error=error.tolist()))
            evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], analytic=result.tolist(), inherited=inherited.tolist(), error=error.tolist()))
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
