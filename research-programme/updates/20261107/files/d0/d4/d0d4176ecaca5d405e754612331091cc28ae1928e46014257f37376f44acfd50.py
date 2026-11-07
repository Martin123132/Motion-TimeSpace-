from soft_population import *


def main():
    modest()
    folder=ROOT/'results/derived-gaunt-bank'
    folder.mkdir(parents=True,exist_ok=False)
    background=thermal_wave.thermal.ThermalBackground('heavy')
    temperatures=np.geomspace(background.theta0/background.end_scale,background.theta0/background.start_scale,65)
    gaunt=np.array([coefficient(theta,6,6,12)[1] for theta in temperatures])
    interpolator=interpolate.CubicSpline(np.log(temperatures),gaunt,extrapolate=False)
    checks,rows=[],[]
    closed=1+4*np.pi**2/3
    for theta in [1e-7,1e-6,*temperatures[[0,32,-1]]]:
        coarse=coefficient(theta,4,4,8)[1]
        fine=coefficient(theta,6,6,12)[1]
        high=coefficient(theta,8,8,16)[1]
        checks.append(check('Population angular/frequency refinement theta='+str(theta),abs(fine/high-1),2e-10))
        rows.append(dict(theta=float(theta),coarse=coarse,fine=fine,high=high,
                         derived_first_order=1-closed*theta,inherited_inverse=1/(1+14.16*theta),
                         effective_first_order_slope=(1-high)/theta))
    checks.append(check('Exact population integral approaches derived first-order coefficient',abs(rows[0]['effective_first_order_slope']-closed),.002))
    interpolation_errors=[]
    for index in range(0,64,4):
        theta=math.sqrt(temperatures[index]*temperatures[index+1])
        exact_value=coefficient(theta,6,6,12)[1]
        interpolation_errors.append(abs(float(interpolator(math.log(theta)))/exact_value-1))
    checks.append(check('Gaunt table independently checked between knots',max(interpolation_errors),2e-10))
    checks.append(dict(name='Positive derived coefficient across inherited temperature history',passed=bool(np.all(gaunt>0))))
    np.savez_compressed(folder/'gaunt.npz',temperatures=temperatures,gaunt=gaunt)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       knots=len(temperatures),maximum_interpolation_relative_error=max(interpolation_errors),
                       exact_first_order_coefficient=float(closed),gaunt_minimum=float(gaunt.min()),gaunt_maximum=float(gaunt.max()),
                       largest_difference_from_inherited_inverse=float(np.max(abs(gaunt*(1+14.16*temperatures)-1))),
                       soft_photon_population_coefficient=True,full_finite_frequency_relativistic_gaunt=False),__file__,
           [ROOT/'soft_population.py',ROOT/'resolved_redistribution.py',ROOT/'results/derived-soft-coefficient/status.json',
            folder/'gaunt.npz',background.native_constants,background.parent.source])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows,
                          maximum_interpolation_error=max(interpolation_errors))),flush=True)


if __name__=='__main__':
    main()
