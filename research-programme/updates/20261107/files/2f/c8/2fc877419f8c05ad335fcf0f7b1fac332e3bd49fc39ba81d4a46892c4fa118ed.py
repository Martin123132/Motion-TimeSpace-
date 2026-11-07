from soft_matching_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    assert review['retained_unaccepted_accuracy_trials'] == []
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    script_hashes = {digest(path) for path in scripts}
    packets = sorted(path for category in ['results', 'banks'] for path in (ROOT / category).glob('*/status.json'))
    checks, inputs, accepted_tests = [], [], 0
    for path in packets:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['script_sha256'] in script_hashes, path
        assert packet['count'] == len(packet['checks']), path
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']), path
        accepted_tests += packet['count']
        for source, expected in packet['input_hashes'].items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
        checks.append(dict(name='Complete and source/hash-bound: ' + path.relative_to(ROOT).as_posix(), passed=True))
        inputs.append(path)
    npz_count = 0
    for path in ROOT.rglob('*.npz'):
        with np.load(path, allow_pickle=False) as saved:
            for name in saved.files:
                array = saved[name]
                if array.dtype.kind in 'biufc':
                    assert np.isfinite(array).all(), (path, name)
        npz_count += 1
    checks.append(dict(name='All new numerical arrays finite and load without pickle', passed=True, files=npz_count))
    citations = [PARENT / 'results/stage-integrity.json', PARENT / 'mandl_skyrme.py', PARENT / 'gould_angles.py',
        PARENT / 'results/resolved-infrared-asymptotic/status.json', PARENT / 'results/matched-integrated-parity/status.json',
        BRANCH / 'polarized-heat-momentum-grid-20261007/grid_common.py',
        BRANCH / 'expanding-thermal-gravity-20261007/build_spectral_kernel.py',
        BRANCH / 'scaled-spectral-evolution-20261007/sources/2005.06941v1.html',
        HISTORY / 'results/production-primary-refit/status.json']
    provenance = json.loads((ROOT / 'sources/provenance.json').read_text())
    urls = ['https://doi.org/10.1016/0375-9474(94)90698-X', 'https://doi.org/10.1103/PhysRevD.44.3955',
        'https://arxiv.org/html/2005.06941v1', 'https://doi.org/10.1088/1475-7516/2020/10/025']
    for source in provenance['sources']:
        assert digest(source['path']) == source['sha256']
        citations.append(Path(source['path']))
        urls.append(source['url'])
    for path in citations:
        assert path.is_file(), path
    sources_text = (ROOT / 'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in sources_text for url in urls)
    checks.append(dict(name='Local source authorities exist and web source strings are recorded', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    assert not review['full_finite_wavenumber_wave_evolution'] and not review['new_empirical_fit']
    assert not review['complete_finite_radiative_operator'] and not review['arbitrary_nonthermal_soft_extension_proved']
    assert review['physical_number_changing_emission_preserved']
    contract = (ROOT / 'POLE-READ-CONTRACT.md').read_text(encoding='utf-8')
    assert 'hard-process' in contract and 'photon number' in contract
    checks.append(dict(name='Hard-process soft pole distinguished from finite matching and real photon creation', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
        all_current_acceptance_checks_passed=True, checked_packets=len(packets),
        accepted_scientific_checks=accepted_tests, retained_failed_checks=0,
        compiled_scripts=len(scripts), numerical_archives=npz_count, counts_are_tests_not_independent_proofs=True,
        local_citations=[str(path) for path in citations], recorded_web_urls=sorted(set(urls))), __file__,
        [*scripts, *inputs, *citations, ROOT / 'ACCURACY-REVIEW.json', ROOT / 'DERIVATION.md',
         ROOT / 'RESULTS.md', ROOT / 'SOURCES.md', ROOT / 'RESUME.md', ROOT / 'POLE-READ-CONTRACT.md', ROOT / 'sources/provenance.json'])
    print(json.dumps(dict(validation_checks=len(checks), accepted_scientific_checks=accepted_tests,
        packets=len(packets), retained_failed_checks=0, npz=npz_count)), flush=True)


if __name__ == '__main__':
    main()
