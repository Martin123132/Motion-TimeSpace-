from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_joint_first_tangent_20260922 import ProbeMetricRate
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_precise_union_gravity_20260928 import PreciseProbeMassRate
from types import SimpleNamespace
from time import perf_counter
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-probe-gravity-precision-validation-attempt01', __file__)
    started = perf_counter()
    try:
        parent_path = evidence.output.parent / 'annular-live-support-acceleration-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('live_response_complete', parent['state'] == 'complete')
        digests = dict(parent['inputs'], **parent['outputs'])

        def read(relative):
            path = evidence.root / relative
            evidence.check('source_hash:' + relative, hashlib.sha256(path.read_bytes()).hexdigest() == digests[relative])
            evidence.own(path)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {key: archive[key] for key in archive.files}

        rows = []
        for case in parent['cases']:
            name = case['branch'] + '-' + case['level']
            authority = read(case['sources']['parent'])
            centre = next(row for row in authority['centres'] if row.get('route') == 'resampled') if case['level'] == 'fine' else authority['centres'][0]
            flow = read(centre['flow_path'])
            probes = {}
            for index in range(3):
                for sign in [-1, 1]:
                    suffix = '-inner' + str(index) + '-sign' + str(sign) + '.npz'
                    archive = read(next(path for path in centre['probe_paths'] if path.endswith(suffix)))
                    solver, solution = reconstructed_solver(archive)
                    probes[index, sign] = SimpleNamespace(solver=solver, solution=solution)
            coordinate = ProbeMetricRate(probes, flow['inner_steps'])
            precise = PreciseProbeMassRate(coordinate)
            grid = probes[2, 1].solver
            indices = np.unique(np.linspace(0, len(grid.lengths) - 1, 151).astype(int))
            radius = grid.edges[indices] + .371 * grid.lengths[indices]
            value60, value80 = precise.evaluate(radius, 60), precise.evaluate(radius, 80)
            original = coordinate.values(radius)[-1, 0]
            scale = float(np.max(abs(value60)))
            precision_error = float(np.max(abs(value60 - value80)))
            float_error = float(np.max(abs(value60 - original)))
            evidence.check(name + ':nonvacuous_interior_samples', scale > 1e-15, scale)
            evidence.check(name + ':precision60_80', precision_error <= 1e-26, precision_error)
            evidence.check(name + ':finite', np.isfinite(value60).all() and np.isfinite(original).all())
            path = evidence.output / (name + '-interior-samples.npz')
            np.savez_compressed(path, radius=radius, value60=value60, value80=value80, original=original)
            evidence.own(path, 'outputs')
            rows.append(dict(branch=case['branch'], level=case['level'], samples=len(radius),
                derivative_scale=scale, precision60_80_difference=precision_error,
                original_float_difference=float_error))
        path = evidence.output / 'interior-probe-precision.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, scope='Nonzero interior arithmetic validation, not a new finite-difference truncation certificate')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
