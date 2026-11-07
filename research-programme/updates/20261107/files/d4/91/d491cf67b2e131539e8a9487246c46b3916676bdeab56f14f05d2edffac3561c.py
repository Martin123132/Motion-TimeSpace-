from __future__ import annotations

from boundary_common import *
from derive_matter_correction import coefficients


def main():
    modest()
    folder=ROOT/'results/seed-constraints'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    inputs=[ROOT/'derive_matter_correction.py',GEOMETRY/'constraint_common.py']
    for label in ['heavy','cold']:
        path=ROOT/'results/corrected-boundary'/(label+'-orthogonal-seed.npz')
        details_path=ROOT/'results/corrected-boundary'/(label+'-comparison.json')
        inputs.extend([path,details_path])
        packet=np.load(path)
        details=json.loads(details_path.read_text())
        tau=float(packet['tau'])
        fraction=float(packet['neutrino_fraction'])
        baryon_share=details['baryon_share']
        constants=coefficients(fraction,baryon_share)
        total=packet['momentum_p']+packet['momentum_q']
        connections=[]
        for metric,momentum in [(packet['seed_p'],packet['momentum_p']),(packet['seed_q'],packet['momentum_q'])]:
            derivative=1j*np.einsum('a,ij->aij',momentum,metric)
            connections.append(inherited.inherited.christoffel_linear(derivative))
        errors=[]
        for order in ['leading','matter','opacity']:
            rates=[]
            for curvature in [packet['ricci_p'],packet['ricci_q'],packet['ricci2']]:
                scalar=np.trace(curvature)
                tracefree=curvature-np.eye(3)*scalar/3
                if order=='leading':
                    value=tau*(constants['shear0']*tracefree-np.eye(3)*scalar/24)
                elif order=='matter':
                    value=tau**2*(constants['shear_matter']*tracefree+np.eye(3)*scalar/80)
                else:
                    value=tau**2*constants['shear_collision']*tracefree
                rates.append(value)
            rate2=rates[2]
            geometric=1j*total*np.trace(rate2)-1j*total@rate2
            for connection,rate in [(connections[0],rates[1]),(connections[1],rates[0])]:
                for component in range(3):
                    geometric[component]+=.5*sum(-connection[upper,upper,middle]*rate[middle,component]+connection[middle,upper,component]*rate[upper,middle] for upper in range(3) for middle in range(3))
            weighted0=(1-fraction)*constants['photon0']+fraction*constants['neutrino0']
            if order=='leading':
                coefficient=4*tau*weighted0
            elif order=='matter':
                coefficient=tau**2*(4*((1-fraction)*constants['photon_matter']+fraction*constants['neutrino_matter']-.5*weighted0)+3*baryon_share*constants['photon0'])
            else:
                coefficient=4*tau**2*((1-fraction)*constants['photon_collision']+fraction*constants['neutrino_collision'])
            matter_source=1j*total*float(packet['scalar2'])*coefficient
            error=float(np.max(abs(geometric-matter_source)))/max(float(np.max(abs(matter_source))),1e-12)
            errors.append(error)
        checks.append(dict(name=label+': full Fourier gradient3 momentum including connection products',passed=max(errors)<2e-11,relative_errors_by_order=errors))
        checks.append(dict(name=label+': generated metric remains symmetric',passed=bool(np.max(abs(packet['metric2']-packet['metric2'].T))<2e-13)))
        checks.append(dict(name=label+': independent primordial response not assigned or omitted',passed=bool(not packet['primordial_zeta2_value_assigned'] and np.linalg.norm(packet['primordial_metric2_per_zeta2'])>0 and abs(packet['primordial_dust_density2_per_zeta2'])>0)))
        checks.append(dict(name=label+': full and corrected seed scope flags retained',passed=bool(not packet['full_coupled_second_order_solution'] and packet['matter_and_opacity_first_corrections_included'] and packet['finite_gradient4_and_second_matter_order_required'])))
        print(json.dumps(dict(model=label,momentum_relative_errors=errors)),flush=True)
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,
        actual_exported_nonparallel_seed_checked=True,leading_gradient_equations_only=True,
        complete_finite_wavelength_evolution_not_claimed=True),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()
