from thermal_source_common import *
import mpmath as mp


def main():
    modest()
    mp.mp.dps=60
    folder=ROOT/'results/moving-bath-route'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    temperature=mp.mpf('.00045962015785263325')
    for speed_text in ['.01','.03','.1','.5']:
        speed=mp.mpf(speed_text)
        gamma=1/mp.sqrt(1-speed**2)
        directional=lambda cosine:temperature/(gamma*(1+speed*cosine))
        moment=mp.quad(lambda cosine:directional(cosine)**2,[-1,0,1])/2
        checks.append(check('Directional bath preserves scalar leading mass shift beta='+speed_text,abs(moment/temperature**2-1),1e-50))
        for cosine_text in ['-.9','.2','.7']:
            cosine=mp.mpf(cosine_text)
            rest_energy=temperature*mp.mpf('.6')
            bath_energy=gamma*rest_energy*(1+speed*cosine)
            scalar=1/mp.expm1(bath_energy/temperature)
            directional_value=1/mp.expm1(rest_energy/directional(cosine))
            checks.append(check('Moving-electron bath occupation is covariant beta='+speed_text+' cosine='+cosine_text,
                                abs(scalar/directional_value-1),1e-50))
        rows.append(dict(speed=float(speed),minimum_directional_temperature_over_bath=float(directional(1)/temperature),
                         maximum_directional_temperature_over_bath=float(directional(-1)/temperature)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       angle_dependent_temperature_rule_derived=True,moving_loop_angular_average_not_yet_computed=True),__file__)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
