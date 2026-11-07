from reduced_amplitude import *
import ordered_real_kernel as scalar


def main():
    modest()
    exact.mp.mp.dps=75
    folder=ROOT/'results/reduced-amplitude'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    for energy in ['.00045962015785263325','.1','1']:
        for fraction in ['1e-9','.001','.3','-.3','-3']:
            sample=exact.event(energy,fraction,[.7,.2,-.3],[-.3,.5,.6])
            hard_direction=np.array(list(sample['directions'][1]),float)
            soft_direction=np.array(list(sample['directions'][2]),float)
            accelerated=event(float(energy),float(energy)*float(fraction),hard_direction,soft_direction)
            fast=tensor(accelerated)
            reference=exact.tensor_for_event(sample)
            label=' E='+energy+' signed_share='+fraction
            checks.append(check('On-shell-reduced amplitude versus high-precision six diagrams'+label,
                                np.linalg.norm(fast-reference)/np.linalg.norm(reference),2e-12))
            response=mueller(fast)
            checks.append(check('Full Stokes map versus high precision'+label,
                                np.linalg.norm(response-mueller(reference))/np.linalg.norm(response),2e-12))
            for ward in [0,1,2]:
                checks.append(check('Reduced amplitude Ward leg '+str(ward)+label,
                                    np.linalg.norm(tensor(accelerated,ward=ward))/np.linalg.norm(fast),5e-10))
            worst=0.
            for component in [1,2,3]:
                for sign in [-1,1]:
                    stokes=np.eye(4)[0]+sign*np.eye(4)[component]
                    output=response@stokes
                    worst=max(worst,(np.linalg.norm(output[1:])-output[0])/response[0,0])
            checks.append(check('Physical pure input polarizations remain inside Stokes cone'+label,worst,1e-12))
            rows.append(dict(energy=float(energy),signed_share=float(fraction),
                             amplitude_relative_error=float(np.linalg.norm(fast-reference)/np.linalg.norm(reference))))
    sample=event(.01,.0001,np.array([math.sqrt(.99),0,.1]),np.array([0,.8,.6]))
    checks.append(dict(name='Removing a reduced diagram breaks Ward cancellation',
                       passed=np.linalg.norm(tensor(sample,ward=1,omit=(0,1,2)))>1e-5*np.linalg.norm(tensor(sample))))
    for energy in ['.00045962015785263325','.1','1']:
        direction=[math.sqrt(.99),0,.1]
        tree,final=exact.single_tensor(energy,direction)
        incoming=exact.mp.mpf(energy)
        outgoing=incoming/(1+incoming*exact.mp.mpf('.9'))
        expected=2*scalar.compton(-incoming,outgoing)
        checks.append(check('Tree intensity normalization equals2U E='+energy,abs(mueller(tree)[0,0]/float(expected)-1),1e-13))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       reduction_exact_before_float_evaluation=True,spin_and_polarization_preserved=True),__file__,
           [ROOT/'reduced_amplitude.py',AMPLITUDE_PARENT/'dirac_amplitude.py',VACUUM/'ordered_real_kernel.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],maximum_error=max(row['amplitude_relative_error'] for row in rows))),flush=True)


if __name__=='__main__':
    main()
