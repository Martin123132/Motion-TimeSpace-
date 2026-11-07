from __future__ import annotations

from transport_common import *


def main():
    modest()
    folder=ROOT/'results/conserved-flow'
    folder.mkdir(parents=True,exist_ok=False)
    packets={label:np.load(ROOT/'results/continuity'/(label+'.npz')) for label in ['heavy','cold','lcdm']}
    reference=packets['lcdm']
    mode=int(np.argmin(abs(reference['modes']-.03)))
    initial=int(np.argmin(abs(reference['scales']-.5)))
    final=int(np.argmin(abs(reference['scales']-1/1.38)))
    normalization=max(abs(reference['conserved'][mode,final]),abs(2*reference['density_sync'][mode,initial]-3*reference['eta'][mode,initial]))
    rows=[]
    for label,packet in packets.items():
        assert packet['modes'][mode]==.03
        initial_matter=float(packet['conserved'][mode,initial]);final_matter=float(packet['conserved'][mode,final])
        integral=final_matter-initial_matter
        for bias in [1.,2.]:
            initial_tracer=float(bias*packet['density_sync'][mode,initial]-3*packet['eta'][mode,initial])
            final_tracer=initial_tracer+integral
            for magnitude in [.01,.05,.2,.5]:
                amplitude=magnitude/normalization
                coupling=amplitude*integral
                mass_errors=[]
                for count in [512,2048,8192]:
                    phase=(np.arange(count)+.5)*2*math.pi/count
                    mapped,jacobian=flow_map(phase,coupling)
                    initial_density=1+amplitude*initial_tracer*np.cos(phase)
                    final_density=initial_density/jacobian
                    inverse_phase,_=flow_map(phase,-coupling)
                    _,inverse_jacobian=flow_map(inverse_phase,coupling)
                    eulerian_density=(1+amplitude*initial_tracer*np.cos(inverse_phase))/inverse_jacobian
                    mass_errors.append(float(abs(np.mean(eulerian_density)-1)))
                harmonics=[np.mean(initial_density*np.exp(-1j*order*mapped)) for order in [0,1,2,3]]
                linear_prediction=amplitude*final_tracer/2
                linear_error=float(abs(harmonics[1]-linear_prediction))
                step=1e-5
                upper,_=flow_map(phase,coupling+step);lower,_=flow_map(phase,coupling-step)
                path_error=float(np.max(abs((upper-lower)/(2*step)+np.sin(mapped))))
                _,jacobian_upper=flow_map(phase+step,coupling)
                map_upper,_=flow_map(phase+step,coupling);map_lower,_=flow_map(phase-step,coupling)
                jacobian_error=float(np.max(abs((map_upper-map_lower)/(2*step)-jacobian)))
                rows.append(dict(branch=label,initial_bias=bias,amplitude_magnitude=magnitude,
                    primordial_mode_amplitude=float(amplitude),common_normalization=float(normalization),
                    native_integrated_velocity=integral,initial_coordinate_transfer=initial_tracer,final_coordinate_linear_transfer=final_tracer,
                    integrated_flow_amplitude=coupling,min_initial_density=float(min(initial_density)),
                    min_jacobian=float(min(jacobian)),min_final_density=float(min(final_density)),
                    mass_errors=mass_errors,pointwise_mass_error=float(max(abs(final_density*jacobian-initial_density))),
                    path_equation_error=path_error,jacobian_error=jacobian_error,
                    harmonics_real=[float(value.real) for value in harmonics],harmonics_imag=[float(value.imag) for value in harmonics],
                    fundamental_linear_absolute_error=linear_error,linear_prediction=linear_prediction,
                    nonlinear_Euler_convective_source_normalized_max=float(amplitude**2*packet['velocity'][mode,final]**2/2),
                    self_consistent_nonlinear_gravity=False))
                if bias==1 and magnitude==.5:
                    np.savez_compressed(folder/(label+'.npz'),initial_phase=phase,mapped_phase=mapped,jacobian=jacobian,
                        initial_density=initial_density,final_density_on_trajectories=final_density,eulerian_phase=phase,eulerian_density=eulerian_density)
    finish(folder,dict(rows=rows,k_Mpc_inverse=.03,initial_z=1.,final_z=.38,new_parameters_fitted=0,
        flow_scope='Exact positive continuity solution for the prescribed native linear single-mode velocity; nonlinear Euler/metric feedback is not solved.'),
        __file__,[ROOT/'results/continuity/status.json',*[ROOT/'results/continuity'/(label+'.npz') for label in packets],*folder.glob('*.npz')])
    print(json.dumps([row for row in rows if row['initial_bias']==1 and row['amplitude_magnitude']==.5],indent=2))


if __name__=='__main__':
    main()
