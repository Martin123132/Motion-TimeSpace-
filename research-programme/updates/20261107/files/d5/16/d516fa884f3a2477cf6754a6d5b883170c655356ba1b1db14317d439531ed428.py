from __future__ import annotations

from seed_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def check(name,passed,measured=None):
        checks.append(dict(name=name,passed=bool(passed),measured=measured))
    derivation=json.loads((ROOT/'results/derivation/status.json').read_text())
    covariant=json.loads((ROOT/'results/covariant-check/status.json').read_text())
    geometry=json.loads((ROOT/'results/geometry/status.json').read_text())
    native=json.loads((ROOT/'results/native-seed-valid/status.json').read_text())
    for packet in [derivation,covariant]:
        for row in packet['checks']:
            check(row['name'],row['passed'],row['residual'])
    for fraction in [0.,.4,.6]:
        for amplitude in [.01,.03]:
            rows=[row for row in geometry['rows'] if row['neutrino_fraction']==fraction and row['amplitude']==amplitude and row['count']==256]
            tag='Rnu='+str(fraction)+' epsilon='+str(amplitude)
            rows=sorted(rows,key=lambda row:row['tau'],reverse=True)
            for key in ['hamiltonian_relative','momentum_relative']:
                ratios=[rows[index][key]/rows[index+1][key] for index in range(2)]
                check(tag+' '+key+' gradient convergence',all(3.5<ratio<4.5 for ratio in ratios),ratios)
                check(tag+' '+key+' smallest-time gate',rows[-1][key]<.005,rows[-1][key])
            check(tag+' positive metric and conserved cold mass',all(row['min_spatial_metric_factor']>0 and row['mass_jacobian_error']<1e-12 for row in rows))
            fine=next(row for row in geometry['rows'] if row['neutrino_fraction']==fraction and row['amplitude']==amplitude and row['count']==512)
            middle=rows[1]
            change=max(abs(fine[key]-middle[key]) for key in ['hamiltonian_relative','momentum_relative'])
            check(tag+' spatial resolution stability',change<1e-7,change)
            check(tag+' flat divergence is a failed negative control',rows[-1]['wrong_flat_divergence_relative']>100*rows[-1]['momentum_relative'])
    gauge=geometry['gauge_pullback']
    ratios=[gauge[index]['correct_pullback_error']/gauge[index+1]['correct_pullback_error'] for index in range(2)]
    check('quadratic coordinate pullback converges at expected amplitude order',all(3.5<ratio<4.5 for ratio in ratios),ratios)
    check('omitting coordinate pullback produces finite wrong coefficient',gauge[-1]['omitted_pullback_error']>.5 and gauge[-1]['correct_pullback_error']<1e-4)
    primary=[row for row in native['rows'] if row['primary']]
    check('all45 primary branch/quantity/mode comparisons present',len(primary)==45,len(primary))
    for row in primary:
        tag=row['branch']+' '+row['quantity']+' k='+str(row['k_Mpc_inverse'])
        check(tag+' native initial-data recovery',row['qualified'] and row['max_relative_error']<.01,row['max_relative_error'])
    parameters=[]
    for metadata in native['native_metadata']:
        label=metadata['branch']
        packet=np.load(ROOT/'results/native-seed-valid'/(label+'.npz'))
        names=packet['names'].tolist()
        check(label+' actual nonzero native export times',np.all(packet['values'][:,:,names.index('a')]>0))
        check(label+' radiation-dominated seed surface',max(metadata['cold_to_radiation'])<.001,max(metadata['cold_to_radiation']))
        if label=='lcdm':
            continue
        table=np.load(BACKGROUND if label=='heavy' else BRANCH/'native-two-field-transfer-20261007/runs/backgrounds/cold.npz')
        scales=packet['scales']
        beta=packet['beta']
        radiation=packet['photon']+packet['neutrino']+packet['nu']
        for suffix,title in [('s','slow'),('h','heavy')]:
            if suffix=='h' and label!='heavy':
                continue
            coordinate=table['heavy_efold'] if suffix=='h' else table['efold']
            field=interpolate.CubicSpline(coordinate,table['phi_'+suffix])(np.log(scales))
            momentum=interpolate.CubicSpline(coordinate,table['phidot_'+suffix])(np.log(scales))
            mass=float(table[title+'_mass_mpc'])
            ratio=(scales**2*momentum**2+scales**4*mass**2*field**2)/(2*radiation)
            mass_ratio=mass*scales**2/beta
            parameters.append(dict(branch=label,field=title,max_mass_over_H=float(max(mass_ratio)),max_field_to_radiation=float(max(ratio))))
            check(label+' '+title+' frozen and subdominant',max(mass_ratio)<.002 and max(ratio)<1e-5,parameters[-1])
    for path in native['source_backed_seed_paths']:
        packet=np.load(path)
        check('seed scalar adiabatic ratio '+Path(path).name,np.allclose(packet['radiation_first'],4*packet['cold_first']/3,rtol=1e-14,atol=0))
        for title in ['slow','heavy']:
            check('seed second-order momentum '+title+' '+Path(path).name,
                np.allclose(packet[title+'_field_prime_second_native_extension'],
                    6*packet[title+'_field_second_native_extension']/packet['tau'],rtol=1e-14,atol=0))
        check('initial-state choice retained '+Path(path).name,float(packet['primordial_zeta_second'])==0)
    check('failed premature query retained but not accepted',(ROOT/'results/native-seed/FAILED.md').exists() and not (ROOT/'results/native-seed/COMPLETE').exists())
    check('no late nonlinear or fitted claim',not native['late_nonlinear_prediction'] and native['new_parameters_fitted']==0)
    success=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=success,
        symbolic_count_included=derivation['count']+covariant['count'],seed_regime=parameters,
        full_radiation_onset_evolution_validated=False),
        __file__,[ROOT/'results'/name/'status.json' for name in ['derivation','covariant-check','geometry','native-seed-valid']]+[BACKGROUND])
    print(json.dumps(dict(state='complete',checks=len(checks),all_checks_passed=success,
        failures=[row for row in checks if not row['passed']],seed_regime=parameters),indent=2))
    assert success


if __name__=='__main__':
    main()
