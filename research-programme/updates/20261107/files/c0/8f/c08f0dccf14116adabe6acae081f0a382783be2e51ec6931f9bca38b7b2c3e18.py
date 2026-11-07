from emission_angular_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    excluded = set(review['retained_unaccepted_accuracy_trials'])
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    script_hashes = {digest(path) for path in scripts}
    packets = sorted(path for category in ['results', 'banks', 'backgrounds'] for path in (ROOT / category).glob('*/status.json'))
    checks, inputs = [], []
    accepted_tests, retained_failed_checks = 0, 0
    for path in packets:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['script_sha256'] in script_hashes, path
        assert packet['count'] == len(packet['checks']), path
        relative = path.relative_to(ROOT).as_posix()
        if relative in excluded:
            assert not packet['all_checks_passed'] and any(not row['passed'] for row in packet['checks'])
            retained_failed_checks += sum(not row['passed'] for row in packet['checks'])
        else:
            assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']), path
            accepted_tests += packet['count']
        for source, expected in packet['input_hashes'].items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
        checks.append(dict(name='Complete/hash-bound and correctly classified: ' + relative, passed=True))
        inputs.append(path)
    assert retained_failed_checks == review['retained_failed_checks_expected'] and len(excluded) == 1
    rescued = json.loads((ROOT / review['rescued_bank_validation']).read_text())
    assert rescued['all_checks_passed'] and len(rescued['validated_numerical_archives']) == 13
    checks.append(dict(name='Failed eventwise parity diagnostic preserved with separate integral validation', passed=True))
    npz_count = 0
    for path in ROOT.rglob('*.npz'):
        with np.load(path, allow_pickle=False) as saved:
            for name in saved.files:
                array = saved[name]
                if array.dtype.kind in 'biufc':
                    assert np.isfinite(array).all(), (path, name)
        npz_count += 1
    checks.append(dict(name='All new numerical arrays finite and load without pickle', passed=True, files=npz_count))
    citations = [PARENT / 'results/stage-integrity.json', PARENT / 'banks/infrared104-q700/status.json',
        PARENT / 'density/heavy-tangent104-6400/history.npz', PARENT / 'density/cold-tangent104-6400/history.npz',
        HISTORY / 'results/production-primary-refit/status.json', BACKGROUND / 'increment_emitting_geometry.py',
        BACKGROUND / 'dense_geometry_derivative.py', BRANCH / 'mixed-bath-transport-20261007/stable_pair.py']
    provenance = json.loads((ROOT / 'sources/provenance.json').read_text())
    urls = []
    for source in provenance['sources']:
        assert digest(source['path']) == source['sha256']
        citations.append(Path(source['path']))
        urls.extend([source[key] for key in ['url', 'doi'] if key in source])
    for path in citations:
        assert path.is_file(), path
    sources_text = (ROOT / 'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in sources_text for url in urls)
    checks.append(dict(name='Local source authorities exist and web source strings are recorded', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    assert not review['full_finite_wavenumber_wave_evolution'] and not review['new_empirical_fit']
    assert not review['complete_polarized_double_compton_kernel'] and not review['virtual_radiative_matching_completed']
    checks.append(dict(name='Resolved intensity kernel not mislabelled inclusive polarized transport or a sky fit', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
        all_current_acceptance_checks_passed=True, checked_packets=len(packets),
        accepted_scientific_checks=accepted_tests, retained_failed_checks=retained_failed_checks,
        excluded_packets=sorted(excluded), compiled_scripts=len(scripts), numerical_archives=npz_count,
        counts_are_tests_not_independent_proofs=True,
        local_citations=[str(path) for path in citations], recorded_web_urls=sorted(set(urls))), __file__,
        [*scripts, *inputs, *citations, ROOT / 'ACCURACY-REVIEW.json', ROOT / 'DERIVATION.md',
         ROOT / 'RESULTS.md', ROOT / 'SOURCES.md', ROOT / 'RESUME.md', ROOT / 'sources/provenance.json'])
    print(json.dumps(dict(validation_checks=len(checks), accepted_scientific_checks=accepted_tests,
        packets=len(packets), retained_failed_checks=retained_failed_checks, npz=npz_count)), flush=True)


if __name__ == '__main__':
    main()
