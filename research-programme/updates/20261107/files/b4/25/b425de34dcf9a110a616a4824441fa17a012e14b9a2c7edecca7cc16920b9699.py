import re
from thermal_vertex_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    assert not (folder/'COMPLETE').exists()
    folder.mkdir(parents=True,exist_ok=True)
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
    assert accepted==351 and len(packets)==13,(accepted,len(packets))
    citations=[PARENT/'results/stage-integrity.json',AMPLITUDE_PARENT/'dirac_amplitude.py',
               PARENT/'ordered_real_kernel.py',HISTORY/'results/production-primary-refit/status.json']
    documents=[ROOT/name for name in ['DERIVATION.md','RESULTS.md','SOURCES.md','RESUME.md']]
    for document in documents:
        for reference in re.findall(r'`([^`]+)`',document.read_text(encoding='utf-8')):
            if reference.endswith(('.py','.md','.npz','.json','.html','.pdf','.png')):
                path=(ROOT/reference).resolve()
                if path==ROOT/'results/stage-integrity.json':
                    continue
                assert path.is_file(),(document,reference)
                citations.append(path)
    sources=json.loads((ROOT/'sources/provenance.json').read_text())['sources']
    urls=['https://samirvarma.com/publications/']
    for source in sources:
        assert digest(source['path'])==source['sha256']
        citations.append(Path(source['path']))
        urls.append(source['url'])
        if 'doi' in source:
            urls.append(source['doi'])
    source_text=(ROOT/'SOURCES.md').read_text(encoding='utf-8')
    assert all(url in source_text for url in urls)
    citations=sorted(set(citations))
    for path in citations:
        assert path.is_file(),path
    checks.append(dict(name='Every cited local path exists; primary web strings and bytes recorded',passed=True))
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    assert review['thermal_soft_cancellation_from_actual_diagrams']
    assert review['finite_dressed_thermal_amplitude_at_rest']
    assert not review['finite_real_virtual_thermal_rate_matched']
    assert not review['complete_finite_temperature_polarized_operator']
    assert not review['new_empirical_fit'] and not review['medium_electron_uniform_error_bound']
    assert not review['new_finite_wavenumber_wave_evolution']
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='Finite amplitude scope not promoted to full rate, empirical fit or medium-loop bound',passed=True))
    negative_controls=[]
    for packet_name in ['ward-and-dressing','external-residue-soft-match']:
        packet=json.loads((ROOT/'results'/packet_name/'status.json').read_text())
        negative_controls.extend(row for row in packet['checks'] if any(word in row['name'] for word in ['Omitting','Missing','Internal-only']))
    assert negative_controls and all(row['passed'] for row in negative_controls)
    checks.append(dict(name='Negative controls detect missing physical pieces rather than only self-consistency',passed=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,all_current_acceptance_checks_passed=True,
                       checked_packets=len(packets),accepted_scientific_checks=accepted,retained_failed_checks=0,
                       compiled_scripts=len(scripts),local_citations=[str(path) for path in citations],
                       recorded_web_urls=sorted(set(urls)),counts_are_tests_not_independent_proofs=True),__file__,
           [*scripts,*inputs,*citations,*documents,ROOT/'ACCURACY-REVIEW.json',ROOT/'sources/provenance.json'])
    print(json.dumps(dict(validation_checks=len(checks),accepted_scientific_checks=accepted,packets=len(packets),scripts=len(scripts))),flush=True)


if __name__=='__main__':
    main()
