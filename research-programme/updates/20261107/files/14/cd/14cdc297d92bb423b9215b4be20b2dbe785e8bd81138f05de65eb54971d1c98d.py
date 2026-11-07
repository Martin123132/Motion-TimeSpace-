from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import load_npz
import argparse
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', default='annular-position-reaction-diagnostic-attempt04')
    parser.add_argument('--label', default='annular-position-quadrature-components-attempt01')
    args = parser.parse_args()
    if not args.parent or any(character not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for character in args.parent):
        parser.error('A local evidence label is required')
    evidence = EvidenceRun(args.label, __file__)
    try:
        parent_path = evidence.output.parent/args.parent/'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_settled', parent['state'] in ['complete', 'failed'] and parent['diagnostic_only'])
        digests = dict(parent['inputs'], **parent['outputs'])

        def own(relative):
            path = (evidence.root/relative).resolve()
            key = str(path.relative_to(evidence.root))
            if hashlib.sha256(path.read_bytes()).hexdigest() != digests[key]:
                raise RuntimeError('Changed component input: '+key)
            evidence.own(path)
            return path

        def arrays(relative):
            with np.load(own(relative), allow_pickle=False) as archive:
                return {name: archive[name].copy() for name in archive.files}

        rows = []
        for case in parent['cases']:
            branch, level = case['branch'], case['level']
            short = 'reference' if branch == 'reference-reference' else branch
            owner_name = 'annular-'+short+('-matched-current-attempt01' if level == 'fine' else '-third-current-attempt02')
            owner_relative = str((evidence.output.parent/owner_name/'status.json').relative_to(evidence.root))
            owner = json.loads(own(owner_relative).read_text())
            centre = next(row for row in owner['centres'] if row.get('route') == 'resampled') if level == 'fine' else owner['centres'][0]
            lower, higher = [arrays(case['paths']['material'+str(order)]) for order in [48, 64]]
            inverse = BandedSourceInverse(load_npz(own(centre['matrix_path'])), higher['residual'].shape)
            norm = lambda value: float(np.max(np.abs(inverse.solve(value.ravel()))))
            parts = dict(momentum=lower['momentum_rate']-higher['momentum_rate'],
                wave_force=higher['force_wave']-lower['force_wave'],
                native_force=higher['force_native']-lower['force_native'])
            difference = lower['residual']-higher['residual']
            total = norm(difference)
            recorded = case['summary']['material_inverse_error']
            evidence.check(branch+'-'+level+':saved_quadrature_norm_replay',
                abs(total-recorded) <= 64*np.finfo(float).eps*max(abs(recorded), 1e-300),
                dict(recomputed=total, recorded=recorded))
            if branch == 'reference-reference':
                evidence.check(branch+'-'+level+':native_disabled', not np.any(parts['native_force']))
            source_only = np.zeros_like(difference)
            source_only[:, -1] = difference[:, -1]
            field_only = difference-source_only
            row = dict(branch=branch, level=level, total_inverse=total,
                momentum_inverse=norm(parts['momentum']), wave_force_inverse=norm(parts['wave_force']),
                native_force_inverse=norm(parts['native_force']),
                source_only_inverse=norm(source_only), field_only_inverse=norm(field_only),
                floating_decomposition_difference_inverse=norm(difference-sum(parts.values())),
                valid_for_claim=False)
            evidence.report['cases'].append(row)
            rows.append(row)
            evidence.save()
            print(json.dumps(row), flush=True)
        path = evidence.output/'quadrature-components.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(scope='Saved paired-rule discrepancy decomposed with the same inherited inverse',
            diagnostic_only=True, accepted_for_C0=False, full_live_sensitivity_recomputed=False,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
