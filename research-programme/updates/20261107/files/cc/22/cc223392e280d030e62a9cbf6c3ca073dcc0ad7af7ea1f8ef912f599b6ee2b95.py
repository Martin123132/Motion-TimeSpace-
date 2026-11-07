from thermal_radial import *


def independently_integrated(location):
    delta=mp.mpf('1e-7')*min(location,mp.mpf(1))
    def excluded(width):
        return (mp.quad(lambda value:planck_moment(value)/(value**2-location**2),[0,location-width])
                +mp.quad(lambda value:planck_moment(value)/(value**2-location**2),[location+width,location+1,mp.inf]))
    return 2*excluded(delta/2)-excluded(delta)


def main():
    modest()
    mp.mp.dps=65
    folder=ROOT/'results/radial-poles'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows,kernels=[],[],[]
    for location in ['.03','.1','.3','1','2','10','50']:
        scaled=mp.mpf(location)
        direct=thermal_hilbert(scaled)
        special=(mp.log(scaled/(2*mp.pi))-mp.re(mp.digamma(mp.j*scaled/(2*mp.pi))))/2
        excluded=independently_integrated(scaled)
        checks.append(check('Subtracted PV versus Binet digamma z='+location,abs(direct-special),1e-24))
        checks.append(check('Independent symmetric-excision PV z='+location,abs(direct-excluded),1e-18))
        kernels.append(dict(pole_over_temperature=float(scaled),principal_value=float(direct),
                            high_energy_approximation=float(-mp.pi**2/(6*scaled**2))))
    initial=mp.matrix([1,0,0,0])
    for energy_text in ['.00045962015785263325','.01','.1']:
        energy=mp.mpf(energy_text)
        incoming=spin.photon(energy,spin.unit([0,0,1]))
        for direction_index,coordinates in enumerate([[.7,.2,.3],[.3,-.6,-.2]]):
            hard_direction,bath_direction=spin.unit(coordinates),spin.unit([-.2,.8,-.1])
            outgoing=spin.photon(energy/(1+energy*(1-hard_direction[2])),hard_direction)
            final=initial+incoming-outgoing
            for polarization in [0,1]:
                first_pol=spin.frame(spin.unit([0,0,1]))[polarization]
                second_pol=spin.frame(hard_direction)[1-polarization]
                coefficients=radial_decomposition(initial,incoming,outgoing,first_pol,second_pol,bath_direction)
                label=' E='+energy_text+' dir='+str(direction_index)+' pol='+str(polarization)
                for ratio in ['.03','.3','.9','1.2','3','20']:
                    radial=energy*mp.mpf(ratio)
                    original=compton(initial,incoming,outgoing,first_pol,second_pol,spin.photon(radial,bath_direction))
                    rebuilt=reconstruct(coefficients,radial)
                    checks.append(check('Algebraic matrix partial fractions'+label+' k/E='+ratio,mp.norm(original-rebuilt)/mp.norm(original),1e-48))
                finite=finite_radial(coefficients,energy)
                direct=spin.spinors(final).transpose_conj()*spin.gamma_matrices()[0]*finite*spin.spinors(initial)
                poles=[dict(pole_over_temperature=float(pole['location']/energy),
                            bose_occupation=float(1/mp.expm1(pole['location']/energy)),
                            original_denominator_slope_sign=int(pole['denominator_slope_sign'])) for pole in coefficients['poles']]
                checks.append(dict(name='Internal poles are thermally populated'+label,passed=all(.1<item['bose_occupation']<2 for item in poles)))
                rows.append(dict(energy=float(energy),direction=direction_index,polarization=polarization,
                                 finite_radial_amplitude_real_norm=float(mp.norm(direct.apply(mp.re))),
                                 finite_radial_amplitude_imaginary_norm=float(mp.norm(direct.apply(mp.im))),
                                 unintegrated_soft_matrix_norm=float(mp.norm(coefficients['soft'])),poles=poles))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows,
                       universal_pv_kernels=kernels,rational_coefficients_from_exact_residues_not_fits=True,
                       thermal_radial_regular_part_computed=True,angular_integral_not_yet_performed=True,
                       soft_external_residue_cancellation_not_yet_combined=True,finite_width_introduced=False,
                       imaginary_part_is_feynman_cut_not_yet_a_kinetic_rate=True),__file__,
           [ROOT/'thermal_radial.py',ROOT/'thermal_insertions.py',PARENT/'sources/Varma1992.pdf'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],kernels=kernels,first_row=rows[0])),flush=True)


if __name__=='__main__':
    main()
