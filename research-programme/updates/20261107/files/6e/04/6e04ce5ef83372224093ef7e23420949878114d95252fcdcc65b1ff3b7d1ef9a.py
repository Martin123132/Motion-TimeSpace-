from __future__ import annotations

import re
import urllib.request
import sympy as symbolic
from collision_common import *


def main():
    modest()
    folder=ROOT/'results/calibration'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'sources'
    source_folder.mkdir(parents=True,exist_ok=True)
    url='https://physics.nist.gov/cuu/Constants/Table/allascii.txt'
    request=urllib.request.Request(url,headers={'User-Agent':'MTS-private-source-audit/1.0'})
    with urllib.request.urlopen(request,timeout=40) as response:
        contents=response.read()
    table_path=source_folder/'nist-codata-2022.txt'
    table_path.write_bytes(contents)
    lines=contents.decode('utf-8').splitlines()
    def constant(name):
        matches=[]
        for line in lines:
            fields=re.split(r'\s{2,}',line.strip())
            if fields and fields[0]==name:
                matches.append(fields)
        assert len(matches)==1,(name,matches)
        fields=matches[0]
        return dict(value=float(fields[1].replace(' ','')),uncertainty=fields[2],units=fields[3] if len(fields)>3 else '',source_line='  '.join(fields))
    names=['classical electron radius','Thomson cross section','electron mass energy equivalent','Boltzmann constant']
    constants={name:constant(name) for name in names}
    cosine,radius=symbolic.symbols('mu r_e',real=True)
    angular=symbolic.integrate(symbolic.pi*radius**2*(1+cosine**2),(cosine,-1,1))
    checks=[]
    checks.append(dict(name='Unpolarized Maxwell/Poynting cross section integrates to8pi r_e^2/3',passed=symbolic.simplify(angular-8*symbolic.pi*radius**2/3)==0))
    calculated=8*np.pi*constants['classical electron radius']['value']**2/3
    reference=constants['Thomson cross section']['value']
    agreement=abs(calculated/reference-1)
    checks.append(dict(name='Rounded CODATA radius reproduces Thomson value',passed=agreement<3e-10,relative_difference=agreement))
    native_text=(NATIVE/'fortran/constants.f90').read_text()
    match=re.search(r'sigma_thomson\s*=\s*([0-9.eE+-]+)_dl',native_text)
    assert match
    native_sigma=float(match.group(1))
    directions,weights=np.polynomial.legendre.leggauss(96)
    photon_nodes,photon_weights=np.polynomial.legendre.leggauss(160)
    photon_energy=30*(photon_nodes+1)
    planck_weights=30*photon_weights*photon_energy**3/np.expm1(photon_energy)
    planck_weights/=np.sum(planck_weights)
    rows=[]
    for scale in [1e-9,1e-6,1e-5,.0002,.000225,.000265]:
        temperature=2.7255/scale
        thermal_ratio=constants['Boltzmann constant']['value']*temperature/constants['electron mass energy equivalent']['value']
        energy_ratio=photon_energy[:,None]*thermal_ratio
        scattered_ratio=1/(1+energy_ratio*(1-directions))
        kernel=(3/8)*scattered_ratio**2*(scattered_ratio+1/scattered_ratio-1+directions**2)
        cross=kernel@weights
        recoil=(kernel*(1-scattered_ratio))@weights
        momentum=(kernel*(1-scattered_ratio*directions))@weights
        rows.append(dict(scale=scale,temperature_K=temperature,thermal_energy_over_electron_rest=thermal_ratio,
            energy_weighted_KN_total_over_Thomson=float(planck_weights@cross),
            energy_weighted_KN_momentum_over_Thomson=float(planck_weights@momentum),
            cold_electron_recoil_energy_per_Thomson=float(planck_weights@recoil)))
    checks.append(dict(name='Cold-electron recoil diagnostics positive and bounded',passed=all(0<row['energy_weighted_KN_total_over_Thomson']<=1 and row['cold_electron_recoil_energy_per_Thomson']>=0 for row in rows)))
    assert all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,constants=constants,
        sigma_from_radius_m2=calculated,native_sigma_m2=native_sigma,native_relative_offset_from_current_CODATA=native_sigma/reference-1,
        source_url=url,source_release='2022 CODATA as served by NIST',retrieved_utc=datetime.now(timezone.utc).isoformat(),
        new_charge_or_electron_mass_derivation=False,calibration_not_a_fit=True,
        recoil_rows=rows,recoil_diagnostic_not_full_thermal_Compton_operator=True,
        photon_temperature_for_diagnostic_K=2.7255,native_constants_not_changed=True),__file__,[table_path,NATIVE/'fortran/constants.f90'])
    print(json.dumps(dict(sigma_m2=reference,radius_agreement=agreement,native_offset=native_sigma/reference-1)),flush=True)


if __name__=='__main__':
    main()
