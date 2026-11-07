import re
from thermal_source_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=sorted((ROOT/'results').glob('*/status.json'))
    checks,inputs,accepted=[],[],0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file(),path
        assert packet['script_sha256'] in script_hashes,path
        assert packet['count']==len(packet['checks']),path
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']),path
        for source,expected in packet['input_hashes'].items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
        accepted+=packet['count']
        checks.append(dict(name='Immutable completed packet: '+path.parent.name,passed=True))
        inputs.append(path)
    assert accepted==212 and len(packets)==16,(accepted,len(packets))
    documents=[ROOT/name for name in ['DERIVATION.md','RESULTS.md','SOURCES.md','RESUME.md']]
    citations=[PARENT/'results/stage-integrity.json',HISTORY/'results/production-primary-refit/status.json']
    for document in documents:
        for reference in re.findall(r'`([^`]+)`',document.read_text(encoding='utf-8')):
            if reference.endswith(('.py','.md','.npz','.json','.html','.pdf','.png')):
                path=(ROOT/reference).resolve()
                assert path.is_file(),(document,reference)
                citations.append(path)
    citations=sorted(set(citations))
    urls=['https://arxiv.org/html/2005.06941v1','https://doi.org/10.1103/PhysRevD.46.3630',
          'https://samirvarma.com/assets/pdf/Finite-temperature-radiative-corrections-to-Compton-scattering.pdf',
          'https://dlmf.nist.gov/5.9#E15']
    source_text=(ROOT/'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in source_text for url in urls)
    checks.append(dict(name='Every cited local path exists and primary web strings are recorded',passed=True))
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    assert review['finite_conditional_thermal_source_matched'] and review['dressed_state_measure_derived']
    assert review['real_reverse_weak_form_derived'] and review['finite_matching_profile_cancels']
    assert not review['full_thermal_gas_collision_source']
    assert not review['complete_finite_temperature_polarized_operator']
    assert not review['medium_electron_uniform_error_bound']
    assert not review['physical_photon_number_source_projected_to_zero']
    assert not review['new_empirical_fit'] and not review['new_finite_wavenumber_wave_evolution']
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='Conditional source distinguished from full thermal operator and photon number',passed=True))
    matching=json.loads((ROOT/'results/matched-source-validation/status.json').read_text())
    assert matching['all_checks_passed'] and matching['finite_matching_profile_cancels']
    controls=[row for row in matching['checks'] if 'Dropping' in row['name'] or 'multiplier' in row['name']]
    assert len(controls)==4 and all(row['passed'] for row in controls)
    checks.append(dict(name='Matching-profile and scalar-rescaling negative controls pass',passed=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,all_current_acceptance_checks_passed=True,
                       checked_packets=len(packets),accepted_scientific_checks=accepted,retained_failed_checks=0,
                       compiled_scripts=len(scripts),local_citations=[str(path) for path in citations],
                       recorded_web_urls=urls,counts_are_tests_not_independent_proofs=True),__file__,
           [*scripts,*inputs,*citations,*documents,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(validation_checks=len(checks),accepted_scientific_checks=accepted,packets=len(packets),scripts=len(scripts))),flush=True)


if __name__=='__main__':
    main()
