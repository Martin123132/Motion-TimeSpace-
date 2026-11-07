import re
from weak_common import *


def main():
    modest()
    folder = ROOT / 'results/validation'
    folder.mkdir(parents=True, exist_ok=False)
    scripts = sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(), str(script), 'exec')
    hashes = {digest(script) for script in scripts}
    statuses = sorted((ROOT / 'results').glob('*/status.json'))
    checks, paths, count = [], [], 0
    for path in statuses:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and (path.parent / 'COMPLETE').is_file(), path
        assert packet['script_sha256'] in hashes, path
        assert packet['count'] == len(packet['checks']), path
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']), path
        for source_path, expected in packet['input_hashes'].items():
            assert Path(source_path).is_file() and digest(source_path) == expected, (path, source_path)
        for array_path in path.parent.glob('*.npz'):
            with np.load(array_path) as arrays:
                for name in arrays.files:
                    assert np.isfinite(arrays[name]).all(), (array_path, name)
            paths.append(array_path)
        count += packet['count']
        paths.append(path)
        checks.append(dict(name='Immutable result packet: ' + path.parent.name, passed=True))
    assert len(statuses) == 23 and count == 107, (len(statuses), count)
    documents = [ROOT / name for name in ['DERIVATION.md', 'RESULTS.md', 'SOURCES.md', 'RESUME.md']]
    citations = set()
    for document in documents:
        for reference in re.findall(r'`([^`]+)`', document.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.py', '.json', '.npz', '.pdf', '.html')):
                path = (ROOT / reference).resolve()
                if path == ROOT / 'results/stage-integrity.json':
                    continue
                assert path.is_file(), (document, reference)
                citations.add(path)
    urls = ['https://authors.library.caltech.edu/records/hpgb4-8p134',
            'https://doi.org/10.1103/PhysRev.85.231',
            'https://doi.org/10.1103/PhysRevD.46.3630',
            'https://arxiv.org/html/2005.06941v1',
            'https://arxiv.org/abs/hep-ph/9607206']
    assert all(url in (ROOT / 'SOURCES.md').read_text(encoding='utf-8') for url in urls)
    checks.append(dict(name='Local source citations and recorded external URLs exist in provenance', passed=True))
    checks.append(dict(name='All scripts compile without bytecode or new dependency installation', passed=True))
    assert not list(ROOT.rglob('__pycache__'))
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    for field in ['finite_virtual_weak_scalar_projection_completed',
                  'vacuum_and_thermal_matching_completed_at_conditional_scalar_level',
                  'elastic_half_factor_derived', 'displaced_observables_included',
                  'fixed_canonical_momentum_and_population_terms_included',
                  'absorptive_scalar_zero_derived_and_checked', 'absorptive_polarized_terms_retained']:
        assert review[field], field
    for field in ['full_thermal_gas_collision_source', 'complete_finite_temperature_polarized_operator',
                  'physical_photon_number_source_projected_to_zero', 'actual_nonthermal_infrared_occupation_derived',
                  'new_background_evolution', 'new_finite_wavenumber_wave_evolution',
                  'new_empirical_fit', 'new_parent_theory']:
        assert not review[field], field
    checks.append(dict(name='Scalar conditional results are not mislabeled as full gas, polarized or empirical predictions', passed=True))
    comparison = json.loads((ROOT / 'results/matched-weak-validation/status.json').read_text())
    assert comparison['all_checks_passed'] and comparison['chemical_pole_from_current'] > 0
    assert len(review['coarse_chemical_trials_not_production_accuracy']) == 3
    assert comparison['comparisons']['Physical chemical integral radial160 to240 refinement'] < 1e-7
    checks.append(dict(name='Actual chemical source survives and accepted IR quadrature is explicitly refined', passed=True))
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert len(parent['file_hashes']) == 93
    for relative_path, expected in parent['file_hashes'].items():
        assert digest(PARENT / relative_path) == expected, relative_path
    checks.append(dict(name='All93 Stage87 payloads including both source histories remain unchanged', passed=True))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
           all_current_acceptance_checks_passed=True, checked_packets=len(statuses),
           accepted_scientific_checks=count, compiled_scripts=len(scripts),
           local_citations=[str(path) for path in sorted(citations)], recorded_web_urls=urls,
           counts_are_tests_not_independent_proofs=True), __file__,
           [*scripts, *paths, *documents, *citations, ROOT / 'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses), scientific_checks=count,
                         validation_checks=len(checks), scripts=len(scripts))), flush=True)


if __name__ == '__main__':
    main()
