from polarized_source import *


def main():
    modest()
    folder=ROOT/'results/polarized-matching'
    folder.mkdir(parents=True,exist_ok=False)
    names=['rest-a4-r24','rest-a6-r40','moving-a4-r24-v6','moving-a6-r40-v8',
           'moving-profile-point2','moving-a8-r56-v8','reflected-a6-r40-v8']
    datasets,metadata,dependencies={},{},[]
    for name in names:
        source=ROOT/'results'/name/'source.npz'
        status=source.parent/'status.json'
        with np.load(source) as saved:
            datasets[name]={key:saved[key].copy() for key in saved.files}
        metadata[name]=json.loads(status.read_text())
        assert metadata[name]['all_checks_passed']
        dependencies.extend([source,status])
    checks=[]
    for coarse,fine,limit in [('rest-a4-r24','rest-a6-r40',1e-9),
                              ('moving-a4-r24-v6','moving-a6-r40-v8',1e-6),
                              ('moving-a6-r40-v8','moving-a8-r56-v8',1e-9)]:
        difference=datasets[coarse]['lab_fixed_momentum']-datasets[fine]['lab_fixed_momentum']
        for title,selection in [('event',slice(0,1)),('photon force',slice(1,5)),('electron force',slice(5,9))]:
            error=np.linalg.norm(difference[selection])/np.linalg.norm(datasets[fine]['lab_fixed_momentum'][selection])
            checks.append(check('Full Mueller '+title+' refinement '+coarse+' to '+fine,error,limit))
    coarse=datasets['moving-a4-r24-v6']
    fine=datasets['moving-a6-r40-v8']
    checks.append(check('Moving virtual angular6 to8 refinement',np.linalg.norm(coarse['virtual']-fine['virtual'])/np.linalg.norm(fine['virtual']),1e-9))
    for component in [(0,3),(3,0),(2,3),(3,2)]:
        checks.append(check('Phase-sensitive virtual entry refinement '+str(component),
                            abs(coarse['virtual'][component]/fine['virtual'][component]-1),1e-7))
    for name,older in [('rest-a4-r24','thermal-a4-r24'),('rest-a6-r40','thermal-a6-r40')]:
        source=PARENT/'results'/older/'status.json'
        expected=np.array(json.loads(source.read_text())['thermal_correction_vector'])
        dependencies.append(source)
        for index in [0,1,2,4,5,6,8]:
            checks.append(check('Unpolarized rest reduction to prior high-precision source '+name+' row'+str(index),
                                abs(datasets[name]['lab_fixed_momentum'][index,0,0]/expected[index]-1),3e-8))
    profiled=datasets['moving-profile-point2']
    difference=profiled['lab_fixed_momentum']-fine['lab_fixed_momentum']
    for title,selection in [('event',slice(0,1)),('forces',slice(1,9))]:
        checks.append(check('Matching profile cancels for every matrix entry: '+title,
                            np.linalg.norm(difference[selection])/np.linalg.norm(fine['lab_fixed_momentum'][selection]),1e-10))
    parameters=context(.00045962015785263325,.1,[.02,.005,-.01],.00045962015785263325)
    omitted_conversion=lab_moments(profiled['profile_conversion'],parameters)
    conversion_failure=np.linalg.norm(omitted_conversion)/np.linalg.norm(fine['lab_fixed_momentum'])
    checks.append(dict(name='Omitting finite reference conversion demonstrably changes result',passed=bool(conversion_failure>1e-3),relative_change=float(conversion_failure)))
    scalar=fine['lab_fixed_momentum'][0,0,0]*fine['born'][0]
    scalar_failure=np.linalg.norm(fine['lab_fixed_momentum'][0]-scalar)/np.linalg.norm(fine['lab_fixed_momentum'][0])
    checks.append(dict(name='Intensity-only rescaling fails the polarization response',passed=bool(scalar_failure>.01),relative_error=float(scalar_failure)))
    canonical_fraction=np.linalg.norm(fine['canonical_correction'])/np.linalg.norm(fine['lab_fixed_momentum'])
    checks.append(dict(name='Fixed-momentum correction is retained and numerically nonzero',passed=bool(canonical_fraction>1e-5),relative_size=float(canonical_fraction)))
    reflected=datasets['reflected-a6-r40-v8']['lab_fixed_momentum']
    stokes_sign=np.array([1,1,-1,-1])
    moment_sign=np.array([1,1,1,-1,1,1,1,-1,1])
    expected=fine['lab_fixed_momentum']*moment_sign[:,None,None]*stokes_sign[None,:,None]*stokes_sign[None,None,:]
    checks.append(check('Reflection transforms both Stokes indices and four-force',np.linalg.norm(reflected-expected)/np.linalg.norm(expected),1e-9))
    pair=(reflected[0]+fine['lab_fixed_momentum'][0])/2
    odd_indices=[(0,2),(0,3),(1,2),(1,3),(2,0),(3,0),(2,1),(3,1)]
    for entry in odd_indices:
        checks.append(check('Odd reflection entry cancels in symmetric electron pair '+str(entry),
                            abs(pair[entry])/np.linalg.norm(fine['lab_fixed_momentum'][0]),1e-9))
    choi_minima={}
    for name in ['rest-a6-r40','moving-a6-r40-v8','reflected-a6-r40-v8']:
        total=datasets[name]['born'][0]+datasets[name]['lab_fixed_momentum'][0]
        choi=sum(total[first,second]*np.kron(PAULI[first],PAULI[second].T)/2
                 for first,second in itertools.product(range(4),repeat=2))
        minimum=float(np.linalg.eigvalsh(choi).min())
        choi_minima[name]=minimum
        checks.append(check('Total conditional map Choi positivity at benchmark '+name,max(0.,-minimum),1e-12))
    controls=dict(profile_conversion_omission_relative_change=float(conversion_failure),
                  scalar_polarization_rescaling_error=float(scalar_failure),canonical_correction_relative_size=float(canonical_fraction))
    report=dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
                controls=controls,choi_minimum_eigenvalues=choi_minima,
                lab_velocity=[.02,.005,-.01],rest_event_correction=float(datasets['rest-a6-r40']['lab_fixed_momentum'][0,0,0]),
                moving_event_correction=float(fine['lab_fixed_momentum'][0,0,0]),
                conditional_circular_entries_cancel_for_reflected_unpolarized_pair=True,
                positive_benchmark_maps_not_global_positivity_theorem=True,
                full_gas_or_frequency_projection=False)
    finish(folder,report,__file__,[*dependencies,ROOT/'polarized_source.py',ROOT/'moving_frame.py',ROOT/'reduced_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],controls=controls,choi_minima=choi_minima)),flush=True)


if __name__=='__main__':
    main()
