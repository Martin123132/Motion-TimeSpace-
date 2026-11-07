from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from decimal import localcontext
from time import perf_counter
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-original-label-rule-diagnostic-attempt03', __file__)
    started, deadline = perf_counter(), perf_counter() + 3000
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False,
            numerical_acceptance_passed=False, branch='reference-reference', level='fine',
            scope='Original action label resolution; neither representation presumed accurate',
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-original-force-label-resolution.md')
        evidence.own(evidence.root / 'DERIVATION-20260929-high-label-baseline-continuation.md')
        parent_path = evidence.output.parent / 'annular-position-reaction-diagnostic-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        loads, action, sources = restore_case(evidence, digests, 'reference-reference', 'fine', deadline)
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        case = next(row for row in parent['cases'] if row['branch'] == 'reference-reference' and row['level'] == 'fine')
        euler_low, euler_high = [read(case['paths']['material' + str(order)]) for order in [48, 64]]
        original_path = evidence.output.parent / 'annular-position-reaction-attempt01/reference-reference-fine-material64.npz'
        seal_path = evidence.output.parent / 'annular-position-reaction-stage-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('prior_reaction_seal_complete', seal['state'] == 'complete')
        relative = str(original_path.relative_to(evidence.root))
        digests[relative] = seal['hashes'][relative]
        original = load_owned(evidence, digests, original_path)
        resumed_path = evidence.output.parent / 'annular-original-label-rule-diagnostic-attempt02/status.json'
        resumed = json.loads(resumed_path.read_text())
        evidence.own(resumed_path)
        evidence.check('six_original_label_rules_completed',
            resumed['state'] == 'complete' and len(resumed['cases']) == 6
            and all(check['passed'] for check in resumed['checks'])
            and resumed['cases'][-1]['summary']['material_order'] == 512)
        for category in ['inputs', 'outputs']:
            for relative, expected in resumed[category].items():
                if relative == 'CURRENT_LOCAL_RESUME.md':
                    continue
                path = (evidence.root / relative).resolve()
                if not path.is_relative_to(evidence.root) or not path.is_file():
                    raise RuntimeError('Invalid reused input: ' + relative)
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed reused input: ' + relative)
                digests[relative] = expected
                evidence.own(path)
        for case_row in resumed['cases']:
            evidence.report['cases'].append(case_row)
        evidence.report['reused_material_orders'] = [row['summary']['material_order'] for row in resumed['cases']]
        cached = load_owned(evidence, digests, evidence.root / resumed['cases'][-1]['path'])
        previous_force, previous_momentum = cached['force'], cached['momentum']
        rows = [row['summary'] for row in resumed['cases']]
        maximum = lambda array: float(np.max(np.abs(array)))
        with localcontext() as context:
            context.prec = 70
            for order in [1024, 2048]:
                result = action.momentum_and_force(12, order, deadline)
                force, momentum = result['bulk'] + result['dust'], result['momentum']
                evidence.check('finite_original_rule_' + str(order),
                    np.all(np.isfinite(force)) and np.all(np.isfinite(momentum)))
                if order == 64:
                    evidence.check('original64_momentum_replay', maximum(momentum-original['base_momentum']) <= 2e-16,
                        maximum(momentum-original['base_momentum']))
                    evidence.check('original64_force_replay', maximum(force-original['base_force_wave']) <= 2e-15,
                        maximum(force-original['base_force_wave']))
                difference = force - euler_high['base_force_wave']
                location = np.unravel_index(np.argmax(np.abs(difference)), difference.shape)
                row = dict(material_order=order, reference_order=12,
                    force_scale=maximum(force), momentum_scale=maximum(momentum),
                    force_from_original64=maximum(force-original['base_force_wave']),
                    momentum_from_original64=maximum(momentum-original['base_momentum']),
                    force_from_Eulerian24=maximum(force-euler_low['base_force_wave']),
                    force_from_Eulerian32=maximum(difference),
                    momentum_from_Eulerian32=maximum(momentum-euler_high['base_momentum']),
                    field_force_from_Eulerian32=maximum(difference[:, :-1]),
                    source_force_from_Eulerian32=maximum(difference[:, -1]),
                    force_successive_difference=None if previous_force is None else maximum(force-previous_force),
                    momentum_successive_difference=None if previous_momentum is None else maximum(momentum-previous_momentum),
                    maximum_force_difference_label_index=int(location[0]),
                    maximum_force_difference_component=int(location[1]),
                    seconds=perf_counter()-started, valid_for_claim=False)
                path = evidence.output / ('original-label-' + str(order) + '.npz')
                np.savez_compressed(path, momentum=momentum, force=force, bulk=result['bulk'], dust=result['dust'])
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(row), flush=True)
                rows.append(row)
                previous_force, previous_momentum = force, momentum
        path = evidence.output / 'original-label-resolution.csv'
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
