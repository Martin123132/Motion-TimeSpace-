import re
from evolution_common import *


def main():
    modest()
    folder=ROOT/'results/early-scope'
    folder.mkdir(parents=True,exist_ok=False)
    calibration_path=COLLISION/'results/calibration/status.json'
    calibration=json.loads(calibration_path.read_text())
    native_constants=NATIVE/'fortran/constants.f90'
    text=native_constants.read_text()
    def constant(name):
        match=re.search(r'\b'+re.escape(name)+r'\s*=\s*([0-9.eE+-]+)_dl',text,re.I)
        assert match,name
        return float(match.group(1))
    electron_energy=calibration['constants']['electron mass energy equivalent']['value']
    boltzmann=calibration['constants']['Boltzmann constant']['value']
    proton_energy=constant('m_p')*constant('c')**2
    rows=[]
    checks=[]
    sources=[calibration_path,native_constants,NATIVE/'fortran/results.f90',NATIVE/'fortran/equations.f90']
    for label in ['heavy','cold']:
        background=Background(label)
        scales=np.geomspace(5e-7,1e-5,81)
        times=np.array([background.time_at(value) for value in scales])
        native_times=background.native.conformal_time(1/scales-1,tol=1e-10)
        thermal=background.native.get_background_time_evolution(native_times,vars=['opacity','cs2b','T_b','x_e'])
        masses=np.asarray(background.native.nu_masses)
        weights=np.asarray(background.native.grhormass)
        active=weights>0
        ratios=scales[:,None]*masses[active]
        bounds=5*ratios**2/(7*np.pi**2)
        total_bound=bounds@weights[active]/background.radiation
        actual=[]
        for ratio in ratios[-1]:
            difference=integrate.quad(lambda momentum: momentum**2*ratio**2/(math.hypot(momentum,ratio)+momentum)*special.expit(-momentum),0,100,epsabs=1e-15)[0]
            actual.append(difference/(7*np.pi**4/120))
        electron=boltzmann*thermal['T_b']/electron_energy
        proton=boltzmann*thermal['T_b']/proton_energy
        opacity=background.opacity_constant/scales**2
        opacity_error=abs(opacity/thermal['opacity']-1)
        ionization_error=abs(thermal['x_e']/thermal['x_e'][0]-1)
        expansion_error=abs(times/native_times-1)
        temperature_error=abs(thermal['T_b']/(background.native.Params.TCMB/scales)-1)
        source=np.load(background.source)
        field_errors=[]
        for field_index,spline in enumerate(background.field_splines):
            if spline is None:
                field_errors.append(0.)
            else:
                reference=spline(np.log(scales))[:,0]
                predicted=background.solution.sol(times)[field_index+1]
                field_errors.append(float(np.max(abs(reference-predicted))/max(np.max(abs(reference)),1e-100)))
        photon_nodes,photon_weights=np.polynomial.legendre.leggauss(160)
        photon_energy=30*(photon_nodes+1)
        planck=30*photon_weights*photon_energy**3/np.expm1(photon_energy)
        planck/=sum(planck)
        cosine,angular_weights=np.polynomial.legendre.leggauss(96)
        recoil=[]
        for selected in [0,18,80]:
            energy_ratio=photon_energy[:,None]*electron[selected]
            scattered=1/(1+energy_ratio*(1-cosine))
            kernel=(3/8)*scattered**2*(scattered+1/scattered-1+cosine**2)
            recoil.append(dict(scale=float(scales[selected]),thermal_electron_parameter=float(electron[selected]),
                cross_section_fractional_change=float(1-planck@(kernel@angular_weights)),
                momentum_cross_section_fractional_change=float(1-planck@((kernel*(1-scattered*cosine))@angular_weights))))
        rows.append(dict(model=label,scale_range=scales[[0,-1]].tolist(),
            native_mass_over_present_neutrino_temperature=masses[active].tolist(),
            massive_species_energy_fraction_upper_at_endpoint=bounds[-1].tolist(),
            direct_FD_energy_excess_at_endpoint=actual,total_radiation_energy_error_upper=float(max(total_bound)),
            native_baryon_cs2_max=float(max(thermal['cs2b'])),proton_thermal_parameter_max=float(max(proton)),
            electron_thermal_parameter_max=float(max(electron)),native_ionization_relative_variation=float(max(ionization_error)),
            native_opacity_vs_fully_ionized_error=float(max(opacity_error)),native_temperature_vs_photons_error=float(max(temperature_error)),
            self_integrated_time_vs_native_error=float(max(expansion_error)),field_amplitude_envelope_errors=field_errors,
            cold_electron_recoil_diagnostics=recoil,
            neutrino_bound_is_background_energy_not_all_perturbations=True,
            ionization_check_is_native_model_comparison=True,recoil_not_full_thermal_Compton=True))
        checks.extend([
            dict(name=label+': derived FD energy upper bound verified by quadrature',passed=bool(np.all(np.array(actual)<=bounds[-1]*(1+1e-9)))),
            dict(name=label+': numerical background time agrees with native early solution',passed=bool(max(expansion_error)<1e-5),value=float(max(expansion_error))),
            dict(name=label+': retained field backgrounds agree before averaging',passed=bool(max(field_errors)<1e-4),value=max(field_errors)),
            dict(name=label+': native ionization/opacity approximation quantified',passed=bool(max(opacity_error)<1e-4),value=float(max(opacity_error))),
            dict(name=label+': pressureless baryon scope quantified',passed=bool(0<max(thermal['cs2b'])<2e-6),value=float(max(thermal['cs2b']))),
            dict(name=label+': finite electron-temperature limitation retained',passed=bool(max(electron)>1e-4),value=float(max(electron)))])
        np.savez_compressed(folder/(label+'.npz'),scales=scales,times=times,native_times=native_times,neutrino_energy_bounds=bounds,
            total_radiation_bound=total_bound,**thermal)
        sources.append(background.source)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),models=rows,
        physical_prediction_accuracy_not_set_by_numerical_gates=True),__file__,sources)
    print(json.dumps(dict(failures=[row for row in checks if not row['passed']],models=rows)),flush=True)


if __name__=='__main__':
    main()
