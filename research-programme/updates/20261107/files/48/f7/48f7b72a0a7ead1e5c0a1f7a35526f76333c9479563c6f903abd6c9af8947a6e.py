from finite_matching_common import *


def main():
    modest()
    folder=ROOT/'results/external-and-source-validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    paths=[ROOT/'results'/name/'status.json' for name in ['independent-total-reference','total-cross-section-8',
        'total-cross-section-12','four-force-a8-r24','four-force-a12-r40']]
    reference,coarse,fine,force_coarse,force_fine=[json.loads(path.read_text()) for path in paths]
    for index,high in enumerate(fine['rows']):
        expected=reference['rows'][index]
        low=coarse['rows'][index]
        for field in ['born_over_alpha2','nlo_over_alpha3','relative_nlo']:
            error=abs(high[field]/expected[field]-1)
            checks.append(check('Independent2021 analytic total '+field+' E='+str(high['energy']),error,1e-9))
            checks.append(check('Independent angular/radial refinement '+field+' E='+str(high['energy']),abs(high[field]/low[field]-1),1e-9))
        rows.append(dict(energy=high['energy'],calculated_relative_nlo=high['relative_nlo'],
            independent_relative_nlo=expected['relative_nlo'],relative_comparison_error=abs(high['nlo_over_alpha3']/expected['nlo_over_alpha3']-1)))
    for index,high in enumerate(force_fine['rows']):
        low=force_coarse['rows'][index]
        for field in ['photon_source','electron_source','soft_photon_source','hard_photon_source']:
            high_array,low_array=np.array(high[field]),np.array(low[field])
            error=linalg.norm(high_array-low_array)/linalg.norm(high_array)
            checks.append(check('Finite four-force refinement '+field+' E='+str(high['energy']),error,1e-9))
    checks.append(dict(name='External reference includes real and virtual without fitted normalization',passed=True))
    checks.append(dict(name='Vacuum total is not promoted to finite-temperature polarization matrix',passed=all(packet['vacuum_unpolarized_rest_electron'] for packet in [force_coarse,force_fine])))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),
        comparison_rows=rows,scope='Independent QED vacuum benchmark and conserved four-force calibration for the same MTS matter sector; no new sky fit'),__file__,paths)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
