from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_exact_envelope_20261001 import envelope_search
import csv
import ctypes
import hashlib
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 4):
        raise OSError('Cannot pin one CPU')
    evidence = EvidenceRun('annular-repaired-compatibility-attribution-attempt01', __file__)
    verified, rows = {}, []
    try:
        parent_path = evidence.output.parent/'annular-repaired-compatibility-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('parent_complete', parent['state']=='complete' and all(row['passed'] for row in parent['checks']))
        for category in ['inputs', 'outputs']:
            for relative, expected in parent[category].items():
                path = (evidence.root/relative).resolve()
                if not path.is_relative_to(evidence.root) or not path.is_file():
                    raise RuntimeError('Invalid attribution input')
                key = str(path.relative_to(evidence.root))
                if key not in verified:
                    verified[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                    evidence.own(path)
                if verified[key]!=expected:
                    raise RuntimeError('Changed attribution input '+relative)

        def load(short, variant, baseline):
            path = parent_path.parent/(short+'-'+variant+'-'+baseline+'.json')
            if str(path.relative_to(evidence.root)) not in verified:
                raise RuntimeError('Unowned compatibility result')
            return json.loads(path.read_text())

        for short in ['reference', 'MTS']:
            for variant in ['rounded_coefficients', 'parent_nodal']:
                historical = load(short, variant, 'historical')
                fresh = load(short, variant, 'separate_C0_baseline')
                columns = np.array(fresh['columns'])
                column_error = np.array(fresh['column_error'])
                old_base, old_error = [np.array(historical[key]) for key in ['baseline', 'baseline_error']]
                new_base, new_error = [np.array(fresh[key]) for key in ['baseline', 'baseline_error']]
                scenarios = [('historical_central_historical_budget', old_base, old_error, column_error),
                    ('fresh_central_historical_budget', new_base, old_error, column_error),
                    ('historical_central_expanded_budget', old_base, new_error, column_error),
                    ('fresh_central_expanded_budget', new_base, new_error, column_error)]
                for index, label in enumerate(['force', 'h0', 'h1', 'h2']):
                    reduced_error = new_error.copy()
                    reduced_error[index] = old_error[index]
                    scenarios.append(('fresh_reset_'+label+'_budget_to_historical', new_base, reduced_error, column_error))
                for index, label in enumerate(['C0', 'C1', 'C2']):
                    reduced_error = column_error.copy()
                    reduced_error[:, index] = 0
                    scenarios.append(('fresh_zero_'+label+'_error_diagnostic', new_base, new_error, reduced_error))
                outputs = []
                for name, base, error, coefficient_error in scenarios:
                    result = envelope_search(base, columns, error, coefficient_error)
                    witness = result['minimum_scaled_witness']
                    for orthant in result['orthants']:
                        if orthant['exact_witness'] is None:
                            continue
                        exact = orthant['exact_witness']
                        numerator = [int(value) for value in exact['numerator']]
                        denominator = int(exact['denominator'])
                        constraints = [[int(value) for value in row] for row in orthant['exact_constraints']]
                        evidence.check(short+':'+variant+':'+name+':exact_witness_'+str(orthant['signs']),
                            denominator>0 and all(sum(row[index]*numerator[index] for index in range(3))<=row[3]*denominator
                                for row in constraints))
                    row = dict(branch=short, source_variant=variant, scenario=name,
                        exact_sampled_envelope_feasible=result['any_replayed_witness'],
                        exact_sampled_envelope_infeasible=result['exact_infeasibility_proven'],
                        witness_acceleration=None if witness is None else witness['amplitudes'][2],
                        valid_for_claim=False)
                    rows.append(row)
                    outputs.append(dict(summary=row, result=result))
                    print(json.dumps(row), flush=True)
                evidence.check(short+':'+variant+':both_parent_decisions_replayed',
                    outputs[0]['result']['any_replayed_witness']==historical['envelope_search']['any_replayed_witness']
                    and outputs[3]['result']['any_replayed_witness']==fresh['envelope_search']['any_replayed_witness'])
                path = evidence.output/(short+'-'+variant+'-attribution.json')
                with path.open('x', encoding='utf-8') as stream:
                    stream.write(json.dumps(outputs, indent=2, allow_nan=False)+'\n')
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(branch=short, source_variant=variant, path=str(path.relative_to(evidence.root))))
                evidence.save()
        path = evidence.output/'attribution.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with path.open(newline='', encoding='utf-8') as stream:
            parsed = list(csv.DictReader(stream, strict=True))
        evidence.check('csv_valid_44_scenarios', len(parsed)==44 and all(None not in row and row['valid_for_claim']=='False' for row in parsed))
        evidence.own(path, 'outputs')
        evidence.report.update(no_new_fit_parameters=True, numerical_error_ablations_not_physical_promotions=True,
            source_variants_not_selected_for_fit_quality=True, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
