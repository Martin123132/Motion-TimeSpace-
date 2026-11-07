from observer_common import *


def main():
    modest()
    folder = ROOT / 'results/readout-scope'
    folder.mkdir(parents=True, exist_ok=False)
    names = ['coherent36-over32', 'refined-time36', 'band-precision-diagnostic', 'scaled-variable-identities']
    inputs = [ROOT / 'results' / name / 'status.json' for name in names]
    frequency, timing, diagnostic, algebra = [json.loads(path.read_text()) for path in inputs]
    shapes = [row for row in timing['checks'] if 'total shape' in row['name']]
    failed = [row for row in timing['checks'] if not row['passed']]
    checks = [dict(name='All eight global active-shape time comparisons pass the original gate', passed=len(shapes) == 8 and all(row['passed'] for row in shapes)),
              dict(name='Independent wave-basis and ideal-band frequency comparisons pass', passed=frequency['all_checks_passed']),
              dict(name='Open cold x1 time gate explicitly retained, never promoted', passed=len(failed) == 1 and 'cold:' in failed[0]['name'] and 'x=1.0' in failed[0]['name']),
              dict(name='High-precision diagnostic is sourced and complete', passed=diagnostic['all_checks_passed']),
              dict(name='Next evolution-coordinate identities proved without changing physical degrees of freedom', passed=algebra['all_checks_passed'])]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        all_requested_numerical_gates_closed=False, open_time_checks=failed,
                        accepted_scope='Physical readout derivation, qualitative cancellation, global-shape refinement, frequency-band basis refinement, and emission contract. Precision for every individual band is not certified.',
                        latest_coherent_norms=timing['rows'], precision_diagnostic=diagnostic['rows'],
                        no_false_band_pass=True, valid_for_observational_claim=False), __file__, inputs)
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], unresolved_band_time_gates=len(failed))), flush=True)


if __name__ == '__main__':
    main()
