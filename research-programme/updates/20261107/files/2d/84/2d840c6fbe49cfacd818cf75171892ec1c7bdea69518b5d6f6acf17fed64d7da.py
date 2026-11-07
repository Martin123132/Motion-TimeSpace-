from common231 import *
import verify231


def run():
    modest()
    protocol()
    frozen = read(ROOT / 'supplement-configuration.json')
    for name, expected in frozen['hashes'].items():
        assert digest(ROOT / name) == expected
    original = read(ROOT / 'results/local-source.json')
    assert {row['name'] for row in original['failed']} == {'entropy_and_acoustic_characteristic_polynomial', 'canonical_field_off_shell_momentum'}
    original_factor = sp.factor
    diagnostics = []
    def canonical_factor(expression):
        raw = original_factor(expression)
        canonical = sp.cancel(sp.expand(raw))
        if raw != 0 and canonical == 0:
            diagnostics.append(dict(raw=str(raw), canonical=str(canonical)))
        return canonical
    exact_checks = []
    try:
        verify231.sp.factor = canonical_factor
        exact = verify231.symbolic(exact_checks)
    finally:
        verify231.sp.factor = original_factor
    assert len(diagnostics) == 2
    assert all(row['passed'] for row in exact_checks)
    variable = sp.Symbol('test_variable')
    sensitivity = [variable, sp.I * variable, 1 + variable, sp.Rational(1, 10)**40]
    assert all(canonical_factor(value) != 0 for value in sensitivity)
    names = {row['name'] for row in exact_checks}
    final_checks = exact_checks + [row for row in original['checks'] if row['name'] not in names]
    assert len(final_checks) == len(original['checks'])
    assert not (ROOT / 'results/exact-recheck.json').exists()
    report = dict(stage=231, state='complete', finished_at=now(), qualified=all(row['passed'] for row in final_checks),
        checks=final_checks, failed=[row for row in final_checks if not row['passed']], exact=exact,
        raw_normalization=diagnostics, nonzero_sensitivity_controls=len(sensitivity),
        preserved_failed_report_sha256=digest(ROOT / 'results/local-source.json'),
        scope='Exact canonicalization repair only; previous numerical results and equations unchanged')
    write(ROOT / 'results/exact-recheck.json', report)
    print(json.dumps(dict(checks=len(final_checks), failed=report['failed'], normalization=diagnostics)), flush=True)


if __name__ == '__main__':
    run()
