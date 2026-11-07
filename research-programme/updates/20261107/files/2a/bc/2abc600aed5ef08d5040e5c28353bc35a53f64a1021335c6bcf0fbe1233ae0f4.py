from __future__ import annotations

from onset_common import *


def project(phase,values,center,cycles,degree):
    selection=abs(phase-center)<cycles*math.pi
    coordinate=(phase[selection]-center)/(cycles*math.pi)
    columns=[coordinate**power for power in range(degree+1)]
    for harmonic,maximum in [(2,degree-2),(4,2)]:
        for trig in [np.cos,np.sin]:
            columns.extend(coordinate**power*trig(harmonic*phase[selection]) for power in range(maximum+1))
    design=np.array(columns).T
    assert len(design)>4*len(columns)
    coefficients,_,rank,singular=np.linalg.lstsq(design,values[:,selection].T,rcond=None)
    assert rank==len(columns)
    return coefficients[0],float(singular[0]/singular[-1]),int(sum(selection))


def main():
    modest()
    folder=ROOT/'results/occupation'
    folder.mkdir(parents=True,exist_ok=False)
    rows=[]
    variations=[]
    files=[]
    for variant in ['base','early','fine']:
        path=ROOT/'runs'/('heavy-'+variant)/'trajectory.npz'
        packet=np.load(path)
        efold=packet['efold']
        scale=np.exp(efold)
        named={name:packet['values'][index] for index,name in enumerate(packet['names'])}
        mass=float(packet['masses'][1])
        field=named['phi_h']
        velocity=named['dotphi_h']
        response=named['f_h']
        response_dot=named['dotf_h']
        hubble=named['H']
        volume=named['s']
        volume_dot=named['sdot']
        rho=(velocity**2+(mass*field)**2)/2
        pressure=(velocity**2-(mass*field)**2)/2
        energy_response=velocity*response_dot+mass**2*field*response
        pressure_response=velocity*response_dot-mass**2*field*response
        occupation=scale**3*(energy_response+rho*volume)
        occupation_source=-scale**3*(3*(pressure_response+pressure*volume)+pressure*volume_dot/hubble)
        shifted=velocity+1.5*hubble*field
        action0=scale**3*(shifted**2+(mass*field)**2)/2
        action_response=scale**3*(volume*(shifted**2+(mass*field)**2)/2+
            shifted*(response_dot+1.5*hubble*response+.5*volume_dot*field)+mass**2*field*response)
        phase=np.unwrap(np.arctan2(-velocity/mass,field))
        chosen=scale>=.00016
        assert np.all(np.diff(phase[chosen])>0)
        values=np.array([scale**3*rho,occupation,action0,action_response,scale**3*pressure,scale**3*pressure_response])
        for center_scale in [.00019,.00022,.00025]:
            center=float(np.interp(math.log(center_scale),efold,phase))
            for cycles in [4,6,8]:
                for degree in [6,8]:
                    averages,conditioning,count=project(phase,values,center,cycles,degree)
                    rows.append(dict(variant=variant,scale=center_scale,window_halfwidth_pi=cycles,polynomial_degree=degree,
                        sample_count=count,condition_number=conditioning,physical_occupation_response_Mpc2=float(averages[1]/averages[0]),
                        WKB_occupation_response_Mpc2=float(averages[3]/averages[2]),
                        averaged_pressure_over_density=float(averages[4]/averages[0]),
                        averaged_pressure_response_over_density_Mpc2=float(averages[5]/averages[0]),
                        H_over_M=float(np.interp(math.log(center_scale),efold,hubble)/mass)))
        cumulative=integrate.cumulative_simpson(occupation_source[chosen],x=efold[chosen],initial=0)
        residual=occupation[chosen]-occupation[chosen][0]-cumulative
        scale_norm=float(max(abs(occupation[chosen]-occupation[chosen][0])))
        variations.append(dict(variant=variant,
            energy_transport_integral_relative_residual=float(max(abs(residual))/max(scale_norm,1e-90)),
            energy_response_envelope=float(max(abs(energy_response))),
            final_volume_response_Mpc2=float(volume[-1])))
        output=folder/(variant+'.npz')
        np.savez_compressed(output,efold=efold,phase=phase,names=['comoving_rho','physical_occupation','WKB_action','WKB_response','comoving_pressure','comoving_pressure_response'],
            values=values,energy_response=energy_response,occupation_source=occupation_source,transport_residual=residual)
        files.extend([path,output])
    selected=[row for row in rows if row['variant']=='fine' and row['polynomial_degree']==8 and row['window_halfwidth_pi']==6]
    finish(folder,dict(rows=rows,variation_diagnostics=variations,selected_rows=selected,
        interpretation='WKB diagnostic is not a substituted Hilbert energy density. Constancy and matching precision require explicit window/epoch checks.',
        empirical_fit=False),__file__,files)
    print(json.dumps(dict(selected_rows=selected,variation_diagnostics=variations)),flush=True)


if __name__=='__main__':
    main()
