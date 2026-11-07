from thermal_common import *


def main():
    modest()
    folder=ROOT/'results/thermal-scope'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    reports=[]
    inputs=[]
    for label in ['heavy','cold']:
        path=ROOT/'runs'/(label+'-domain')/'spectrum.npz'
        packet=np.load(path)
        background=ThermalBackground(label)
        frequency=np.geomspace(.01,20.,3000)
        spline=interpolate.CubicSpline(np.log(packet['frequency']),packet['potential'])
        potential=spline(np.log(frequency))
        potential_prime=spline(np.log(frequency),1)/frequency
        occupation=planck(frequency)
        equilibrium_weight=weight(frequency)
        temperature=float(packet['temperature_scaled'])
        perturbation=equilibrium_weight*potential
        perturbation_prime=equilibrium_weight*(potential_prime-(1+2*occupation)*potential)
        leading_flux=frequency**4*equilibrium_weight*(potential_prime-temperature)
        omitted_flux=background.chi*frequency**4*(temperature*perturbation_prime+perturbation**2)
        norm=lambda values:math.sqrt(integrate.trapezoid(abs(values)**2,np.log(frequency)))
        flux_residual=norm(omitted_flux)/norm(leading_flux)
        fractional_occupation=background.chi*(1+occupation)*potential
        times=np.linspace(0,background.end,101)
        couplings=[background.at(value) for value in times]
        physical_hubble=np.array([row['hubble']*background.constants['c']/(row['scale']*background.constants['Mpc']) for row in couplings])
        coulomb_estimate=np.array([3e-9*row['scale']**-1.5 for row in couplings])
        separation=physical_hubble/coulomb_estimate
        reference=np.load(PARENT/'results/early-scope'/(label+'.npz'))
        checks.append(dict(name=label+': heat-capacity linearization small in stated frequency band',passed=flux_residual<.001,value=flux_residual,gate=.001))
        checks.append(dict(name=label+': occupation perturbation small in stated band',passed=np.max(abs(fractional_occupation))<.001,value=np.max(abs(fractional_occupation)),gate=.001))
        checks.append(dict(name=label+': assumed one-temperature plasma has estimated rate separation',passed=max(separation)<1e-7,value=float(max(separation)),gate=1e-7,estimate_not_rigorous_microphysical_bound=True))
        reports.append(dict(model=label,finite_chi_omitted_flux_relative_norm=flux_residual,
            maximum_band_occupation_fraction=float(np.max(abs(fractional_occupation))),
            maximum_thermal_parameter=max(row['thermal_parameter'] for row in couplings),
            maximum_frequency_times_thermal_parameter_on_band=20*max(row['thermal_parameter'] for row in couplings),
            hubble_over_estimated_coulomb_rate_max=float(max(separation)),
            thermal_operator_first_nonrelativistic_order=True,full_relativistic_error_not_a_proved_uniform_bound=True,
            low_frequency_photon_production_omitted=True,anisotropic_polarized_thermal_recoil_not_complete=True,
            heat_capacity_linearization_error_test_is_flux_norm_not_global_solution_bound=True))
        inputs.extend([path,PARENT/'results/early-scope'/(label+'.npz')])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),models=reports,
        approximate_coulomb_rate_source='https://arxiv.org/html/1110.0475v2 section1',
        sky_spectrum_prediction_not_claimed=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=reports)),flush=True)


if __name__=='__main__':
    main()
