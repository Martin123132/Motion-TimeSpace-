from finite_matching_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=sorted((ROOT/'results').glob('*/status.json'))
    checks,inputs,failed,accepted=[],[],[],0
    allowed_name='Brown-Feynman low-energy logarithm c=-.9'
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file(),path
        assert packet['script_sha256'] in script_hashes,path
        assert packet['count']==len(packet['checks']),path
        for source,expected in packet['input_hashes'].items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
        rejected=[row for row in packet['checks'] if not row['passed']]
        if rejected:
            assert path.parent.name=='finite-virtual' and len(rejected)==1 and rejected[0]['name']==allowed_name
            assert not packet['all_checks_passed']
            failed.extend(rejected)
        else:
            assert packet['all_checks_passed'],path
        accepted+=sum(row['passed'] for row in packet['checks'])
        checks.append(dict(name='Immutable complete packet with explicit acceptance classification: '+path.parent.name,passed=True))
        inputs.append(path)
    assert len(failed)==1
    authority=json.loads((ROOT/'results/external-and-source-validation/status.json').read_text())
    low_energy=json.loads((ROOT/'results/low-energy-and-real-amplitude/status.json').read_text())
    assert authority['all_checks_passed'] and low_energy['all_checks_passed']
    checks.append(dict(name='Independent total and leading-log replacement gates pass; failed raw threshold retained',passed=True))
    urls=[]
    citations=[PARENT/'results/stage-integrity.json',PARENT/'dirac_amplitude.py',PARENT/'DERIVATION.md',
        BRANCH/'emitting-thermal-background-20261008/DERIVATION.md',
        BRANCH/'scaled-spectral-evolution-20261007/sources/2005.06941v1.html',
        HISTORY/'results/production-primary-refit/status.json']
    for provenance_name in ['provenance.json','additional-provenance.json']:
        provenance_path=ROOT/'sources'/provenance_name
        citations.append(provenance_path)
        for source in json.loads(provenance_path.read_text())['sources']:
            assert digest(source['path'])==source['sha256']
            citations.append(Path(source['path']))
            urls.extend([source['url'],source['doi']])
    urls.extend(['https://authors.library.caltech.edu/records/hpgb4-8p134',
        'https://arxiv.org/html/2005.06941v1','https://samirvarma.com/publications/'])
    source_text=(ROOT/'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in source_text for url in urls)
    for path in citations:
        assert path.is_file(),path
    checks.append(dict(name='Local source citations and web strings recorded and hash-bound',passed=True))
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    assert review['retained_failed_check_count']==1
    assert review['finite_vacuum_real_virtual_matching'] and review['independent_published_total_reproduced']
    assert not review['complete_finite_temperature_polarized_operator'] and not review['new_empirical_fit']
    assert not review['new_finite_wavenumber_wave_evolution'] and review['physical_number_changing_emission_preserved']
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='Vacuum calibration not substituted for thermal polarization or empirical evidence',passed=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,all_current_acceptance_checks_passed=True,
        checked_packets=len(packets),accepted_scientific_checks=accepted,retained_failed_checks=len(failed),
        compiled_scripts=len(scripts),local_citations=[str(path) for path in citations],recorded_web_urls=sorted(set(urls)),
        counts_are_tests_not_independent_proofs=True),__file__,[*scripts,*inputs,*citations,
        ROOT/'ACCURACY-REVIEW.json',ROOT/'DERIVATION.md',ROOT/'RESULTS.md',ROOT/'SOURCES.md',ROOT/'RESUME.md'])
    print(json.dumps(dict(validation_checks=len(checks),accepted_scientific_checks=accepted,
        retained_failed_checks=len(failed),packets=len(packets))),flush=True)


if __name__=='__main__':
    main()
