from wave_common import *


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
    packets = sorted(path for category in ['results', 'banks', 'density'] for path in (ROOT / category).glob('*/status.json'))
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
    assert retained_failed_checks == 2 and len(excluded) == 1
    npz_count = 0
    for path in ROOT.rglob('*.npz'):
        with np.load(path, allow_pickle=False) as saved:
            for name in saved.files:
                array = saved[name]
                if array.dtype.kind in 'biufc':
                    assert np.isfinite(array).all(), (path, name)
        npz_count += 1
    checks.append(dict(name='All new numerical arrays finite and load without pickle', passed=True, files=npz_count))
    citations = [PARENT / 'results/stage-integrity.json', PARENT / 'sources/1109.6552.html',
        PARENT / 'sources/gauntff_merged_Z01.dat', PARENT / 'sources/gauntff_merged_Z02.dat',
        PARENT / 'increment_emitting_geometry.py', PARENT / 'backgrounds/heavy-ir96-integrated-6400/history.npz',
        PARENT / 'backgrounds/cold-ir96-integrated-6400/history.npz',
        BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html',
        BRANCH / 'mixed-bath-transport-20261007/stable_pair.py',
        HISTORY / 'results/production-primary-refit/status.json', ROOT / 'sources/astro-ph-0611172.html']
    for path in citations:
        assert path.is_file(), path
    source = json.loads((ROOT / 'sources/provenance.json').read_text())
    assert digest(source['path']) == source['sha256']
    urls = ['https://arxiv.org/html/astro-ph/0611172', 'https://arxiv.org/html/1109.6552',
            'https://doi.org/10.1111/j.1365-2966.2011.19786.x', 'https://arxiv.org/html/2005.06941v1',
            'https://doi.org/10.1088/1475-7516/2020/10/025', 'https://data.nublado.org/gauntff/']
    sources_text = (ROOT / 'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in sources_text for url in urls)
    checks.append(dict(name='Local source authorities exist and web source strings are recorded', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    assert not review['full_finite_wavenumber_wave_evolution'] and not review['new_empirical_fit']
    checks.append(dict(name='Source milestone not mislabelled a finite-k run or observational fit', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
        all_current_acceptance_checks_passed=True, checked_packets=len(packets),
        accepted_scientific_checks=accepted_tests, retained_failed_checks=retained_failed_checks,
        excluded_packets=sorted(excluded), compiled_scripts=len(scripts), numerical_archives=npz_count,
        local_citations=[str(path) for path in citations], recorded_web_urls=urls), __file__,
        [*scripts, *inputs, *citations, ROOT / 'ACCURACY-REVIEW.json', ROOT / 'DERIVATION.md',
         ROOT / 'RESULTS.md', ROOT / 'SOURCES.md', ROOT / 'RESUME.md', ROOT / 'sources/provenance.json'])
    print(json.dumps(dict(validation_checks=len(checks), accepted_scientific_checks=accepted_tests,
                         packets=len(packets), retained_failed_checks=retained_failed_checks, npz=npz_count)), flush=True)


if __name__ == '__main__':
    main()
