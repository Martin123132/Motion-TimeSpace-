from __future__ import annotations

from boundary_common import *
from derive_matter_correction import coefficients


def main():
    modest()
    folder=ROOT/'results/corrected-boundary'
    folder.mkdir(parents=True,exist_ok=True)
    assert not (folder/'COMPLETE').exists()
    inputs=[ROOT/'derive_matter_correction.py',ROOT/'results/matter-correction/status.json']
    reports=[]
    checks=[]
    for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
        comparison=ROOT/'results/native-boundary'/(label+'-comparison.json')
        source=HISTORY/'runs/sources'/source_name
        thermal_path=PARENT/'runs/backgrounds'/(label+'.npz')
        inputs.extend([comparison,source,thermal_path,ROOT/'results/native-boundary'/(label+'-orthogonal-seed.npz')])
        saved=json.loads(comparison.read_text())
        thermal=np.load(thermal_path)
        params=inherited.inherited.inherited.inherited.inherited.inherited.params_for(source)
        background=inherited.camb.get_background(params)
        beta=float(background.adotrad)
        matter=float((background.grhob+background.grhoc)/(3*beta))
        baryon_share=float(background.grhob/(background.grhob+background.grhoc))
        fraction=saved['neutrino_fraction']
        kappa0=float(thermal['opacity'][0]*thermal['scales'][0]**2/beta**2)
        collision=1/kappa0
        constants=coefficients(fraction,baryon_share)
        rows=[]
        for row in saved['rows']:
            tau=row['tau']
            mode=row['mode']
            curvature=4*mode**2
            density=curvature*tau**2/16*(1-matter*tau/5)
            photon=constants['photon0']*tau**3+(matter*constants['photon_matter']+collision*constants['photon_collision'])*tau**4
            neutrino=constants['neutrino0']*tau**3+(matter*constants['neutrino_matter']+collision*constants['neutrino_collision'])*tau**4
            prediction=[density,density,4*density/3,4*density/3,-4*mode*curvature*photon/3,-4*mode*curvature*neutrino/3]
            reference=np.array(row['native'][:6])
            errors=abs(np.array(prediction)-reference)/np.maximum(np.maximum(np.abs(prediction),abs(reference)),1e-100)
            rows.append(dict(row,predicted_corrected=prediction,relative_errors_corrected=errors.tolist(),
                matter_expansion_parameter=matter*tau,photon_mean_free_path_parameter=collision*tau))
        for mode in [.03,.1,1.]:
            subset=[row for row in rows if np.isclose(row['mode'],mode)]
            selected=subset[-1]
            before=max(selected['relative_errors'][:6])
            after=max(selected['relative_errors_corrected'])
            checks.append(dict(name=label+' k'+str(mode)+': leading matter/opacity correction improves native seed at a1e-6',passed=bool(after<before),before=before,after=after))
        output=dict(model=label,mu=matter,kappa0=kappa0,baryon_share=baryon_share,coefficients=constants,rows=rows,
            approximation='Leading gradient curvature with first matter-loading and photon mean-free-path corrections',
            full_finite_wave_boundary_accuracy_not_certified=True,no_parameter_fitting=True)
        write_json(folder/(label+'-comparison.json'),output)
        with np.load(ROOT/'results/native-boundary'/(label+'-orthogonal-seed.npz')) as old:
            packet={name:old[name].copy() for name in old.files}
        tau=float(packet['tau'])
        scalar=float(packet['scalar2'])
        curvature_tensor=packet['ricci2']-np.eye(3)*scalar/3
        metric_p,metric_q=packet['seed_p'],packet['seed_q']
        def correction_rate(curvature):
            scalar_value=np.trace(curvature)
            tracefree=curvature-np.eye(3)*scalar_value/3
            return (matter*constants['shear_matter']+collision*constants['shear_collision'])*tracefree+np.eye(3)*matter*scalar_value/80
        rate2=correction_rate(packet['ricci2'])
        rate_p=correction_rate(packet['ricci_p'])
        rate_q=correction_rate(packet['ricci_q'])
        packet['metric2']+=(2/3)*tau**3*(rate2+(metric_p@rate_q+metric_q@rate_p)/2)
        packet['mixed_rate2']+=tau**2*rate2
        packet['dust_density2']*=1-matter*tau/5
        packet['radiation_density2']*=1-matter*tau/5
        packet['field2']*=1-matter*tau/35
        packet['field_prime2']*=1-matter*tau/30
        packet['neutrino_mixed_stress2_over_background']-=8*tau**3/45*(matter*constants['shear_matter']+collision*constants['shear_collision'])*curvature_tensor
        packet['photon_mixed_stress2_over_background']=-32*collision*constants['shear0']*tau**3/45*curvature_tensor
        total=packet['momentum_p']+packet['momentum_q']
        packet['covariant_photon_velocity2']=1j*total*scalar*(constants['photon0']*tau**3+(matter*constants['photon_matter']+collision*constants['photon_collision'])*tau**4)
        packet['covariant_neutrino_velocity2']=1j*total*scalar*(constants['neutrino0']*tau**3+(matter*constants['neutrino_matter']+collision*constants['neutrino_collision'])*tau**4)
        primordial_ricci=linear_ricci(seed_linear(total),total)
        packet['primordial_metric2_per_zeta2']+=(2/3)*tau**3*correction_rate(primordial_ricci)
        packet['primordial_mixed_rate2_per_zeta2']+=tau**2*correction_rate(primordial_ricci)
        packet['primordial_dust_density2_per_zeta2']*=1-matter*tau/5
        packet['primordial_radiation_density2_per_zeta2']*=1-matter*tau/5
        packet['primordial_field2_per_zeta2']*=1-matter*tau/35
        packet['primordial_field_prime2_per_zeta2']*=1-matter*tau/30
        packet.update(mu=matter,kappa0=kappa0,matter_and_opacity_first_corrections_included=True,
            finite_gradient4_and_second_matter_order_required=True)
        np.savez_compressed(folder/(label+'-orthogonal-seed.npz'),**packet)
        selected=[row for row in rows if np.isclose(row['mode'],.1)][-1]
        report=dict(model=label,mu=matter,kappa0=kappa0,seed_mode_dot_tau=.1*tau,
            mode1e_minus1_original_errors=selected['relative_errors'][:6],mode1e_minus1_corrected_errors=selected['relative_errors_corrected'])
        reports.append(report)
        print(json.dumps(report),flush=True)
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,models=reports,
        inherited_source_parameters_unchanged=True,primordial_value_still_unassigned=True,
        seed_order_improved_not_exact_finite_wave_initial_solution=True),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()
