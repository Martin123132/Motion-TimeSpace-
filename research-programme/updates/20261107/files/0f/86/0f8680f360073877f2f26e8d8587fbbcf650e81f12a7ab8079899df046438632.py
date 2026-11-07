from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_exact_envelope_20261001 import envelope_search
import csv
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-integrated-baseline-locked-budget-attempt01', __file__)
    try:
        parents = {}
        for name in ['annular-repaired-compatibility-attempt02', 'annular-integrated-baseline-assembly-attempt01']:
            path = evidence.output.parent/name/'status.json'
            report = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+':complete', report['state']=='complete' and all(row['passed'] for row in report['checks']))
            parents[name] = report

        def read(relative, parent):
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=parent['outputs'][relative]:
                raise RuntimeError('Changed locked-budget authority')
            evidence.own(path)
            return json.loads(path.read_text())

        old_parent = parents['annular-repaired-compatibility-attempt02']
        new_parent = parents['annular-integrated-baseline-assembly-attempt01']
        rows = []
        for item in new_parent['summaries']:
            if item['baseline_scenario']!='coefficient_retained_envelope':
                continue
            old_item = next(row for row in old_parent['summaries'] if row['branch']==item['branch']
                and row['source_variant']==item['source_variant'] and row['baseline_variant']=='separate_C0_baseline')
            old, new = read(old_item['path'], old_parent), read(item['path'], new_parent)
            evidence.check(item['branch']+':'+item['source_variant']+':columns_held', old['columns']==new['columns'] and old['column_error']==new['column_error'])
            result = envelope_search(np.array(new['baseline']), np.array(new['columns']), np.array(old['baseline_error']), np.array(new['column_error']))
            row = dict(branch=item['branch'], source_variant=item['source_variant'],
                original_baseline_original_budget=old['envelope_search']['any_replayed_witness'],
                updated_baseline_original_budget=result['any_replayed_witness'],
                updated_baseline_accounted_budget=new['envelope_search']['any_replayed_witness'], valid_for_claim=False)
            rows.append(row)
            path = evidence.output/(item['branch']+'-'+item['source_variant']+'.json')
            with path.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(dict(summary=row, result=result), indent=2)+'\n')
            evidence.own(path, 'outputs')
            print(json.dumps(row), flush=True)
        path = evidence.output/'locked-budget.csv'
        with path.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(comparisons=rows, github_action=False, subagents_used=False, valid_for_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
