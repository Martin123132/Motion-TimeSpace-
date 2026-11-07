from derive_annular_source_gravity_20260914 import EvidenceRun
from diagnose_annular_position_force_20260929 import field_force
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
from time import perf_counter
from decimal import localcontext
import json
import numpy as np


class ZeroResponse:
    def values(self, radius):
        return np.zeros((2, len(radius)))


def main():
    evidence = EvidenceRun('annular-position-metric-force-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        parent_path = evidence.output.parent / 'annular-position-reaction-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live, jets = [status(name) for name in ['annular-live-support-acceleration-attempt01', 'annular-position-metric-jet-validation-attempt01']]
        branch, level = 'reference-reference', 'fine'
        loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
        match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
        previous, jet = map(match, [live, jets])
        directions = read(previous['direction_path'])
        correction = read(previous['paths']['projection'])['correction']
        mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
        owner = read(sources['parent'])
        centre = next(row for row in owner['centres'] if row.get('route') == 'resampled')
        inverse = BandedSourceInverse(load_npz(evidence.root / centre['matrix_path']), loads.rates.shape)
        outputs = {}
        with localcontext() as context:
            context.prec = 70
            for order in [48, 64, 96]:
                result = field_force(loads, action, directions, correction, mode_rate, ZeroResponse(), order, 12)
                path = evidence.output / ('zeroP-force-' + str(order) + '.npz')
                np.savez_compressed(path, **result)
                evidence.own(path, 'outputs')
                original_path = evidence.output.parent / 'annular-position-force-diagnostic-attempt01' / ('force-' + str(order) + '-12.npz')
                evidence.own(original_path)
                with np.load(original_path) as original:
                    result['eulerian_metric'] = original['metric'] - result['metric']
                baseline = outputs.get(48, result)
                comparisons = {key: dict(scale=float(np.max(abs(result[key]))), raw=float(np.max(abs(result[key] - baseline[key]))),
                    inverse=float(np.max(abs(inverse.solve((result[key] - baseline[key]).ravel()))))) for key in result}
                summary = dict(order=order, comparisons=comparisons, seconds=perf_counter() - started)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
                outputs[order] = result
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
