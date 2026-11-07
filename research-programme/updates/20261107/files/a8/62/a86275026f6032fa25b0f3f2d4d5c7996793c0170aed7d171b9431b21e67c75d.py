from __future__ import annotations

from transport_common import *


def time_derivative(values,times,scales,redshift,step):
    center=-math.log1p(redshift)
    middle=int(np.argmin(abs(np.log(scales)-center)))
    offsets=np.arange(-4,1) if redshift==0 else np.arange(-2,3)
    indices=np.array([int(np.argmin(abs(np.log(scales)-(center+offset*step)))) for offset in offsets])
    span=(times[indices[-1]]-times[indices[0]])/(offsets[-1]-offsets[0])
    coordinate=(times[indices]-times[middle])/span
    weights=np.linalg.solve(np.vander(coordinate,5,increasing=True).T,np.array([0.,1.,0.,0.,0.]))/span
    return values[:,indices]@weights,indices,weights


def main():
    modest()
    folder=ROOT/'results/rhs-precision'
    folder.mkdir(parents=True,exist_ok=False)
    summaries=[]
    for label in ['heavy','cold','lcdm']:
        packet,columns=fields(label)
        value=packet['values'];names=packet['names'];fraction=columns['baryon_fraction']
        cold=value[:,:,names.index('delta_cdm')];baryon=value[:,:,names.index('delta_baryon')]
        cold_velocity=value[:,:,names.index('v_newtonian_cdm')];baryon_velocity=value[:,:,names.index('v_newtonian_baryon')]
        density_roundoff=((1-fraction)*abs(np.spacing(cold.astype(np.float32))).astype(float)+fraction*abs(np.spacing(baryon.astype(np.float32))).astype(float))/2
        velocity_roundoff=((1-fraction)*abs(np.spacing(cold_velocity.astype(np.float32))).astype(float)+fraction*abs(np.spacing(baryon_velocity.astype(np.float32))).astype(float))/2
        native_growth=value[:,:,names.index('growth')]
        rows=[]
        for redshift in evolution.TARGET_REDSHIFTS:
            middle=int(np.argmin(abs(packet['scales']-1/(1+redshift))))
            hubble=columns['hubble'][:,middle]
            eta_rate,indices,weights=time_derivative(columns['eta'],packet['times'],packet['scales'],float(redshift),.001)
            eta_coarse,_,_=time_derivative(columns['eta'],packet['times'],packet['scales'],float(redshift),.002)
            density_rate=columns['conserved'][:,indices]@weights/hubble
            rhs_density=native_growth[:,middle]*columns['density_sync'][:,middle]
            rate=columns['velocity'][:,middle];scale=np.maximum(abs(rate),1e-8)
            rhs_residual=(rhs_density-3*eta_rate/hubble-rate)/scale
            fd_residual=(density_rate-rate)/scale
            quantization=(density_roundoff[:,indices]@abs(weights)/hubble+velocity_roundoff[:,middle])/scale
            for mode_index in np.flatnonzero(packet['modes']<=5):
                rows.append(dict(k_Mpc_inverse=float(packet['modes'][mode_index]),z=float(redshift),
                    rhs_residual=float(rhs_residual[mode_index]),time_fd_residual=float(fd_residual[mode_index]),
                    float32_rate_error_bound=float(quantization[mode_index]),
                    metric_derivative_step_change=float(3*abs(eta_rate[mode_index]-eta_coarse[mode_index])/hubble[mode_index]/scale[mode_index])))
        primary=[row for row in rows if row['z']==.38 and .007<=row['k_Mpc_inverse']<=.14]
        summary=dict(branch=label,rows=rows,primary_max_rhs_residual=max(abs(row['rhs_residual']) for row in primary),
            all_max_rhs_residual=max(abs(row['rhs_residual']) for row in rows),
            all_max_metric_derivative_step_change=max(row['metric_derivative_step_change'] for row in rows),
            all_max_time_fd_residual=max(abs(row['time_fd_residual']) for row in rows),
            all_max_float32_rate_bound=max(row['float32_rate_error_bound'] for row in rows),
            exact_float32_density_storage=bool(np.array_equal(cold,cold.astype(np.float32).astype(float)) and np.array_equal(baryon,baryon.astype(np.float32).astype(float))))
        summaries.append(summary)
        print(json.dumps({key:value for key,value in summary.items() if key!='rows'}),flush=True)
    finish(folder,dict(branches=summaries,source_fact='Native GetOutputEvolutionFork writes density/velocity through default-real Arr before copying into double output; native growth and etak are double.',
        primary_native_RHS_target=1e-5,finite_difference_not_exact_conservation_proof=True),__file__,[ROOT/'results/continuity/status.json'])


if __name__=='__main__':
    main()
