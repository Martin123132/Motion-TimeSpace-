from __future__ import annotations

from transport_common import *


def main():
    modest()
    folder=ROOT/'results/continuity'
    folder.mkdir(parents=True,exist_ok=False)
    summaries=[];inputs=[]
    for label in ['heavy','cold','lcdm']:
        packet,columns=fields(label)
        qualified=packet['modes']<=5
        rows=[]
        for redshift in evolution.TARGET_REDSHIFTS:
            index=int(np.argmin(abs(packet['scales']-1/(1+redshift))))
            rate=columns['velocity'][:,index];scale=np.maximum(abs(rate),1e-8)
            fine,actual_fine=derivative(columns['conserved'],packet['scales'],columns['actual_scale'],float(redshift),.001)
            coarse,actual_coarse=derivative(columns['conserved'],packet['scales'],columns['actual_scale'],float(redshift),.002)
            sync,actual_sync=derivative(columns['density_sync'],packet['scales'],columns['actual_scale'],float(redshift),.001)
            _,eta_prime=derivative(columns['eta'],packet['scales'],columns['actual_scale'],float(redshift),.001)
            for mode_index in np.flatnonzero(qualified):
                rows.append(dict(k_Mpc_inverse=float(packet['modes'][mode_index]),z=float(redshift),
                    velocity_transfer=float(rate[mode_index]),conserved_derivative=float(actual_fine[mode_index]),
                    fractional_residual=float((actual_fine[mode_index]-rate[mode_index])/scale[mode_index]),
                    requested_time_residual=float((fine[mode_index]-rate[mode_index])/scale[mode_index]),
                    derivative_step_change=float(abs(actual_fine[mode_index]-actual_coarse[mode_index])/scale[mode_index]),
                    sync_only_residual=float((actual_sync[mode_index]-rate[mode_index])/scale[mode_index]),
                    missing_metric_rate=float(3*eta_prime[mode_index]/scale[mode_index]),
                    density_newtonian_shift_fraction=float((columns['density_newtonian'][mode_index,index]-columns['density_sync'][mode_index,index])/columns['density_sync'][mode_index,index]),
                    coordinate_shift_fraction=float((columns['conserved'][mode_index,index]-columns['density_sync'][mode_index,index])/columns['density_sync'][mode_index,index])))
        primary=[row for row in rows if row['z']==.38 and .007<=row['k_Mpc_inverse']<=.14]
        redshift_one=int(np.argmin(abs(packet['scales']-.5)))
        redshift_final=int(np.argmin(abs(packet['scales']-1/1.38)))
        bias_law=1+columns['density_sync'][:,redshift_one]/columns['density_sync'][:,redshift_final]
        band=(packet['modes']>=.007)&(packet['modes']<=.14)
        summary=dict(branch=label,rows=rows,qualified_modes=int(qualified.sum()),
            primary_max_residual=max(abs(row['fractional_residual']) for row in primary),
            all_max_residual=max(abs(row['fractional_residual']) for row in rows),
            primary_max_sync_defect=max(abs(row['sync_only_residual']) for row in primary),
            all_max_sync_defect=max(abs(row['sync_only_residual']) for row in rows),
            primary_max_derivative_step_change=max(row['derivative_step_change'] for row in primary),
            all_max_derivative_step_change=max(row['derivative_step_change'] for row in rows),
            primary_max_newtonian_density_shift=max(abs(row['density_newtonian_shift_fraction']) for row in primary),
            primary_max_coordinate_density_shift=max(abs(row['coordinate_shift_fraction']) for row in primary),
            conserved_identity_max_error=float(np.max(abs(columns['conserved']-(columns['density_sync']-3*columns['eta'])))),
            baryon_fraction_range=float(np.ptp(columns['baryon_fraction'])),
            actual_requested_scale_max_error=float(np.max(abs(columns['actual_scale']/packet['scales']-1))),
            conserved_initial_bias2_at_z1_final_range=[float(min(bias_law[band])),float(max(bias_law[band]))])
        summaries.append(summary)
        np.savez_compressed(folder/(label+'.npz'),modes=packet['modes'],scales=packet['scales'],
            qualified=qualified,**columns,bias2_evolved=bias_law)
        print(json.dumps({key:value for key,value in summary.items() if key!='rows'}),flush=True)
        inputs.extend([SPECTRUM/'runs'/label/'background.npz',*sorted((SPECTRUM/'runs'/label).glob('chunk-*.npz'))])
    finish(folder,dict(branches=summaries,proper_to_coordinate_density=True,actual_survey_refit=False),
        __file__,[*inputs,*folder.glob('*.npz')])


if __name__=='__main__':
    main()
