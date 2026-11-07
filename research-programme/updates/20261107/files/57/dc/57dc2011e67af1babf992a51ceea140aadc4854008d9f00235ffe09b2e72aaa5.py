from mixed_common import *


def main():
    modest()
    folder = ROOT / 'results/background-closure-review'
    folder.mkdir(parents=True, exist_ok=False)
    checks, inputs, rows = [], [], []
    original = ROOT / 'results/event-and-background-source-refinement/status.json'
    packet = json.loads(original.read_text())
    inputs.append(original)
    event_checks = [row for row in packet['checks'] if ':24-3200:' in row['name']]
    residual_failures = [row for row in packet['checks'] if '-residual:' in row['name'] and not row['passed']]
    assert event_checks and residual_failures and not packet['all_checks_passed']
    checks.extend(dict(row, name='Independent event6/event8 refinement: ' + row['name']) for row in event_checks)
    checks.append(dict(name='Original raw-residual negligibility test stays failed and preserved', passed=True,
                       failed_comparisons=len(residual_failures)))
    for model in ['heavy', 'cold']:
        background = ROOT / 'backgrounds' / model / 'status.json'
        probe = ROOT / 'waves' / (model + '-relaxed-source-probe') / 'status.json'
        for path in [background, probe]:
            report = json.loads(path.read_text())
            assert report['all_checks_passed'] and (path.parent / 'COMPLETE').exists()
            checks.extend(dict(row, name=model + ': balanced replacement: ' + row['name']) for row in report['checks'])
            inputs.append(path)
        report = json.loads(probe.read_text())
        worst = max(row['fraction_of_mixed'] for row in report['rows'] if row['fraction_of_mixed'] is not None)
        rows.append(dict(model=model, largest_relaxed_source_feature_fraction=worst,
                         full_second_order_background_claim=False))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        failed_trial_repaired_by_derived_source_not_relaxed_tolerance=True,
                        failure_mechanism='Raw g_res is not the homogeneous collision after finite-capacity relaxation; E p_prime=-chi(t+t_prime).',
                        accepted_scope='Leading mixed wave on the saved background, plus independently evolved relaxed-background source sensitivity. The complete nonlinear background remains distinct.',
                        raw_source_only_comparison_not_promoted=True), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()
