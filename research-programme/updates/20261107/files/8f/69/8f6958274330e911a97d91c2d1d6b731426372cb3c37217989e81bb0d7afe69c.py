import re
from kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=sorted(list((ROOT/'results').glob('*/status.json'))+list((ROOT/'backgrounds').glob('*/status.json')))
    checks,inputs,accepted=[],[],0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').is_file(),path
        assert packet['script_sha256'] in script_hashes,path
        assert packet['count']==len(packet['checks']),path
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']),path
        for source_path,expected in packet['input_hashes'].items():
            assert Path(source_path).is_file() and digest(source_path)==expected,(path,source_path)
        accepted+=packet['count']
        checks.append(dict(name='Immutable completed packet: '+path.parent.name,passed=True))
        inputs.append(path)
    assert accepted==179 and len(packets)==21,(accepted,len(packets))
    documents=[ROOT/name for name in ['DERIVATION.md','RESULTS.md','SOURCES.md','RESUME.md']]
    citations=[PARENT/'results/stage-integrity.json',HISTORY/'results/production-primary-refit/status.json']
    for document in documents:
        for reference in re.findall(r'`([^`]+)`',document.read_text(encoding='utf-8')):
            if reference.endswith(('.py','.md','.npz','.json','.html','.pdf','.png')):
                path=(ROOT/reference).resolve()
                if path==ROOT/'results/stage-integrity.json':
                    continue
                assert path.is_file(),(document,reference)
                citations.append(path)
    citations=sorted(set(citations))
    urls=['https://arxiv.org/html/2005.06941v1']
    assert all(url in (ROOT/'SOURCES.md').read_text(encoding='utf-8') for url in urls)
    checks.append(dict(name='Cited local paths and external source strings verified',passed=True))
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    for field in ['real_polarized_weak_form_derived','resolved_real_gas_spectrum_block_computed','inverse_reaction_ordering_derived',
                  'weak_soft_counterterm_derived','fixed_density_population_mass_derivative_derived',
                  'soft_first_order_coefficient_derived','soft_population_factor_calculated','both_retained_backgrounds_updated',
                  'old_controls_reproduce_saved_histories','change_itself_time_refined','new_background_evolution']:
        assert review[field],field
    for field in ['full_thermal_gas_collision_source','complete_finite_temperature_polarized_operator',
                  'finite_virtual_weak_projection_completed','physical_photon_number_source_projected_to_zero',
                  'new_finite_wavenumber_wave_evolution','new_empirical_fit','new_parent_theory']:
        assert not review[field],field
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='Updated soft source distinguished from full matched redistribution and observational evidence',passed=True))
    evolved=json.loads((ROOT/'results/evolved-source-comparison/status.json').read_text())
    assert evolved['all_checks_passed'] and len(evolved['rows'])==2
    assert all(row['time_refinement_of_change']<.002 for row in evolved['rows'])
    for model in ['heavy','cold']:
        report=json.loads((ROOT/'backgrounds'/(model+'-derived-gaunt')/'status.json').read_text())
        assert report['derived_soft_gaunt'] and report['bremsstrahlung_included']
        assert not report['full_double_compton_redistribution_included']
    checks.append(dict(name='Both baseline controls and refined source changes verified without double-counting real redistribution',passed=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,all_current_acceptance_checks_passed=True,
                       checked_packets=len(packets),accepted_scientific_checks=accepted,retained_failed_checks=0,
                       compiled_scripts=len(scripts),local_citations=[str(path) for path in citations],recorded_web_urls=urls,
                       counts_are_tests_not_independent_proofs=True),__file__,
           [*scripts,*inputs,*citations,*documents,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(validation_checks=len(checks),accepted_scientific_checks=accepted,packets=len(packets),scripts=len(scripts))),flush=True)


if __name__=='__main__':
    main()
