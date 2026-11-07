from thermal_common import *


def sample(packet,frequencies):
    potential=interpolate.CubicSpline(np.log(packet['frequency']),packet['potential'])(np.log(frequencies))
    return frequencies**3*weight(frequencies)*potential


def spectral_error(first,second):
    frequencies=np.geomspace(.01,20.,2000)
    left=sample(first,frequencies)
    right=sample(second,frequencies)
    measure=np.log(frequencies)
    error=math.sqrt(integrate.trapezoid(abs(left-right)**2,measure)/max(integrate.trapezoid(abs(left)**2,measure),integrate.trapezoid(abs(right)**2,measure),1e-100))
    return error


def main():
    modest()
    folder=ROOT/'results/spectral-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    inputs=[]
    checks=[]
    reports=[]
    principal={}
    for label in ['heavy','cold']:
        packets={}
        for suffix in ['base','time','frequency','domain','fast-limit']:
            path=ROOT/'runs'/(label+'-'+suffix)/'spectrum.npz'
            packets[suffix]=np.load(path)
            inputs.extend([path,path.parent/'status.json'])
        for title,first,second in [('time','base','time'),('frequency','time','frequency'),('frequency_domain','frequency','domain'),('derived_fast_temperature_limit','domain','fast-limit')]:
            error=spectral_error(packets[first],packets[second])
            checks.append(dict(name=label+': '+title,passed=error<.001,value=error,gate=.001))
        packet=packets['domain']
        chi=float(packet['chi'])
        energy=float(packet['energy']@packet['potential'])
        expected=-math.log(10)
        checks.append(dict(name=label+': heat-capacity law from conserved expansion work',passed=abs(energy/expected-1)<1e-7,value=abs(energy/expected-1),gate=1e-7))
        grid=SpectralGrid(1600,1e-5,60)
        temperature=float(packet['temperature_scaled'])
        compton_temperature=-float(grid.energy@grid.apply(packet['potential']))/grid.temperature_energy
        frequencies=np.geomspace(.01,20.,2000)
        full=sample(packet,frequencies)
        y_potential=frequencies**2*(1+2*planck(frequencies))-4*frequencies
        one_shape=(energy/4)*frequencies**3*weight(frequencies)*y_potential
        shape_error=math.sqrt(integrate.trapezoid((full-one_shape)**2,np.log(frequencies))/integrate.trapezoid(full**2,np.log(frequencies)))
        checks.append(dict(name=label+': a single y-shape is not silently substituted',passed=shape_error>.01,value=shape_error,gate_is_rejection_of_y_only_closure=True))
        relative=chi*(1+planck(packet['frequency']))*packet['potential']
        background=ThermalBackground(label)
        points=np.linspace(0,background.end,801)
        integrated_compton=integrate.simpson([background.at(point)['coefficient'] for point in points],x=points)
        reports.append(dict(model=label,chi=chi,final_energy_fraction=chi*energy,leading_heat_capacity_prediction=-chi*math.log(10),
            electron_temperature_fraction=chi*temperature,compton_equilibrium_temperature_fraction=chi*compton_temperature,
            electron_minus_compton_fraction=chi*(temperature-compton_temperature),
            integrated_compton_parameter=integrated_compton,y_only_spectral_error=shape_error,
            maximum_fractional_occupation_distortion=float(np.max(abs(relative))),
            domain_minimum=float(packet['minimum']),domain_maximum=float(packet['maximum']),
            infrared_photon_production_not_included=True,small_heat_capacity_does_not_imply_small_compton_parameter=True))
        principal[label]=packet
    difference=spectral_error(principal['heavy'],principal['cold'])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),models=reports,
        heavy_cold_scaled_spectral_difference=difference,comparison_weight='L2 of x^3 delta n/chi in log x on[.01,20]',
        experimental_detection_not_claimed=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=reports,heavy_cold_scaled_spectral_difference=difference)),flush=True)


if __name__=='__main__':
    main()
