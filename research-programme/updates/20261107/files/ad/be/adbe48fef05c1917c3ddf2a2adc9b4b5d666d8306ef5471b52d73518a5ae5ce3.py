from thermal_vertex_common import *
from emission_rates import ALPHA
import thermal_wave_common as thermal_wave
from consistent_spectral_basis import ConsistentBasis


def main():
    modest()
    folder=ROOT/'results/medium-and-existing-bath'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows,inputs=[],[],[]
    emitting=BRANCH/'emitting-thermal-background-20261008'
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        path=emitting/'backgrounds'/(model+'-ir96-integrated-6400')/'history.npz'
        packet=json.loads((path.parent/'status.json').read_text())
        assert packet['all_checks_passed']
        basis=ConsistentBasis(**packet['basis_spec'])
        with np.load(path) as saved:
            expansion=saved['expansion'].copy()
            profiles=saved['profiles'].copy()
            gas=saved['temperature_scaled'].copy()
        moment_rows=[]
        for count in [700,1000]:
            frequency,measure=thermal_wave.frequency_quadrature(count,basis.minimum,basis.maximum)
            moment_rows.append(basis.evaluate(frequency).T@(measure/frequency)*thermal_wave.I3)
        constants=background.constants
        reduced_compton=6.62607015e-34/(2*np.pi*constants['m_e']*constants['c'])
        for index in [0,len(expansion)//2,len(expansion)-1]:
            scale=background.start_scale*math.exp(expansion[index])
            theta=background.theta0/scale
            electron_theta=theta*(1+packet['heat']*gas[index])
            density=background.electron0/scale**3
            natural_density=density*reduced_compton**3
            fugacity_bound=natural_density*np.pi**2/(electron_theta*special.kve(2,1/electron_theta))
            plasma_ratio=math.sqrt(4*np.pi*ALPHA*natural_density)/theta
            shifts=[packet['heat']*float(moment@profiles[index])/(np.pi**2/6) for moment in moment_rows]
            label=model+' a='+str(scale)
            checks.append(check('Resolved nonthermal mass-moment quadrature '+label,abs(shifts[0]-shifts[1])/max(abs(shifts[1]),1e-20),1e-6))
            checks.append(dict(name='Equilibrium electron occupation bound remains dilute '+label,passed=bool(0<fugacity_bound<1e-10)))
            checks.append(dict(name='Plasma scale below saved spectral floor '+label,passed=bool(0<plasma_ratio<basis.minimum)))
            checks.append(dict(name='No negative electron temperature '+label,passed=bool(electron_theta>0)))
            rows.append(dict(model=model,scale_factor=float(scale),electron_density_m3=float(density),
                             photon_temperature_over_rest_mass=float(theta),electron_temperature_over_rest_mass=float(electron_theta),
                             equilibrium_fermion_occupation_upper_bound=float(fugacity_bound),
                             cold_plasma_energy_over_temperature=float(plasma_ratio),spectral_floor=float(basis.minimum),
                             resolved_distortion_delta_mass_squared_over_Planck_mass_squared=float(shifts[1]),
                             zero_chemical_potential_pair_suppression_not_used=True,
                             omitted_electron_loop_uniform_bound=False,unresolved_bath_below_floor_assigned=False))
        inputs.extend([path,path.parent/'status.json',background.parent.source,background.native_constants])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(item['passed'] for item in checks),rows=rows,
                       same_saved_MTS_histories=True,new_fit=False,
                       fermi_bound_assumes_equilibrium_isotropic_ideal_gas_at_saved_temperature=True,
                       cold_plasma_formula_is_nonrelativistic_leading_order=True,
                       actual_medium_not_assumed_absent=True),__file__,
           [*inputs,BRANCH/'observer-frequency-projection-20261007/consistent_spectral_basis.py',
            BRANCH/'thermal-recoil-and-spectral-response-20261007/thermal_common.py'])
    print(json.dumps(dict(checks=len(checks),failed=[item for item in checks if not item['passed']],rows=rows)),flush=True)


if __name__=='__main__':
    main()
