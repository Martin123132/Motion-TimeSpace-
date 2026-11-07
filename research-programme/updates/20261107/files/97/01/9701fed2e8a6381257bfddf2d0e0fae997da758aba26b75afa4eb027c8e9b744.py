from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from decimal import localcontext
from time import perf_counter
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-original-spatial-rule-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        parent_path = evidence.output.parent / 'annular-position-reaction-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        loads, action, sources = restore_case(evidence, digests, 'reference-reference', 'fine', deadline)
        comparison_path = evidence.output.parent / 'annular-position-reaction-attempt02/reference-reference-fine-material64.npz'
        comparison = load_owned(evidence, digests, comparison_path)
        original_path = evidence.output.parent / 'annular-position-reaction-attempt01/reference-reference-fine-material64.npz'
        evidence.own(original_path)
        with np.load(original_path) as stream:
            original_momentum = stream['base_momentum'].copy()
            original_force = stream['base_force_wave'].copy()
        with localcontext() as context:
            context.prec = 70
            for spatial in [20, 28]:
                result = action.momentum_and_force(spatial, 64, deadline)
                force = result['bulk'] + result['dust']
                path = evidence.output / ('original-spatial-' + str(spatial) + '.npz')
                np.savez_compressed(path, momentum=result['momentum'], force=force)
                evidence.own(path, 'outputs')
                summary = dict(spatial=spatial, momentum_difference_from_12=float(np.max(abs(result['momentum']-original_momentum))),
                    force_difference_from_12=float(np.max(abs(force-original_force))),
                    momentum_difference_from_Eulerian32=float(np.max(abs(result['momentum']-comparison['base_momentum']))),
                    force_difference_from_Eulerian32=float(np.max(abs(force-comparison['base_force_wave']))), seconds=perf_counter()-started)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
