from __future__ import annotations

from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/native-sources'
    folder.mkdir(parents=True,exist_ok=False)
    wanted=[.03,.1,1.]
    records={}
    inputs=[]
    for path in sorted((PARENT/'runs/exact').glob('chunk-*.npz')):
        with np.load(path) as packet:
            matches=[(target,np.flatnonzero(np.isclose(packet['modes'],target,rtol=1e-13,atol=0))) for target in wanted]
            matches=[(target,indices) for target,indices in matches if len(indices)]
            if not matches:
                continue
            inputs.append(path)
            for target,indices in matches:
                assert len(indices)==1 and target not in records
                records[target]=(packet['names'].copy(),packet['values'][indices[0]].copy(),packet['requested_scale'].copy(),packet['conformal_time'].copy())
    assert sorted(records)==wanted
    source=PARENT/'runs/sources/unmatched-base.npz'
    inputs.append(source)
    table=np.load(source)
    params=inherited.inherited.inherited.params_for(source)
    baryon_fraction=params.ombh2/(params.ombh2+params.omch2)
    masses=[float(table['slow_mass_mpc']),float(table['heavy_mass_mpc'])]
    labels=['slow','heavy']
    checks=[]
    def check(name,passed,**details):
        checks.append(dict(name=name,passed=bool(passed),**details))
        assert passed,(name,details)
    names,reference,scales,times=records[.03]
    native_scale_error=0.
    for target,(mode_names,values,requested,conformal) in records.items():
        check(str(target)+': common time and column grids',np.array_equal(mode_names,names) and np.array_equal(requested,scales) and np.array_equal(conformal,times))
        check(str(target)+': exact pre-matching native states',np.all(values[:,list(names).index('mts_match_count')]==0) and np.isfinite(values).all())
        error=float(np.max(abs(values[:,list(names).index('a')]/scales-1)))
        native_scale_error=max(native_scale_error,error)
        check(str(target)+': actual scale agrees with requested scale',error<1e-6,max_relative_error=error)
    output={}
    configurations=[]
    metrics=[]
    exchange_error=0.
    trace_error=0.
    for pnorm,qnorm in [(.03,.03),(.03,.1),(.1,.1),(.1,1.),(1.,1.)]:
        for angle in [-1.,0.,.5,1.]:
            pvector=np.array([pnorm,0.,0.])
            qvector=qnorm*np.array([angle,math.sqrt(max(0,1-angle**2)),0.])
            values_p=records[pnorm][1]
            values_q=records[qnorm][1]
            metric_p=metric(pnorm,pvector/pnorm,names,values_p,baryon_fraction)
            metric_q=metric(qnorm,qvector/qnorm,names,values_q,baryon_fraction)
            geometric=None
            canonical=[]
            for label,mass in zip(labels,masses):
                suffix='s' if label=='slow' else 'h'
                field_p=values_p[:,list(names).index('mts_dphi_'+suffix)]
                field_q=values_q[:,list(names).index('mts_dphi_'+suffix)]
                prime_p=values_p[:,list(names).index('mts_dphidot_'+suffix)]
                prime_q=values_q[:,list(names).index('mts_dphidot_'+suffix)]
                result=vertices(pvector,qvector,metric_p,metric_q,field_p,field_q,prime_p,prime_q,scales,mass)
                swapped=vertices(qvector,pvector,metric_q,metric_p,field_q,field_p,prime_q,prime_p,scales,mass)
                for key,value in result.items():
                    if key=='Einstein_volume_geometric':
                        geometric=value
                        continue
                    output.setdefault(label+'_'+key,[]).append(value)
                    exchange_error=max(exchange_error,float(np.max(abs(value-swapped[key]))/max(float(np.max(abs(value))),1e-300)))
                residual=result['Einstein_volume_canonical']+scales**2*(result['E_quadratic']+3*result['P_quadratic'])/2
                envelope=max(float(np.max(abs(result['Einstein_volume_canonical']))),1e-300)
                trace_error=max(trace_error,float(np.max(abs(residual)))/envelope)
                canonical.append(result['Einstein_volume_canonical'])
            output.setdefault('Einstein_volume_geometric',[]).append(geometric)
            output.setdefault('Einstein_volume_total_source',[]).append(geometric+sum(canonical))
            configurations.append(dict(p_mpc_inverse=pnorm,q_mpc_inverse=qnorm,cosine=angle,
                K_mpc_inverse=float(np.linalg.norm(pvector+qvector)),homogeneous=bool(np.linalg.norm(pvector+qvector)==0)))
            metrics.append(dict(p=metric_p,q=metric_q))
    arrays={key:np.asarray(value) for key,value in output.items()}
    check('Every native source is finite',all(np.isfinite(value).all() for value in arrays.values()))
    check('Exchange symmetry of all field vertices',exchange_error<1e-13,max_relative_error=exchange_error)
    check('Active trace gradient cancellation on native histories',trace_error<1e-12,max_envelope_error=trace_error)
    for label in labels:
        tensor=arrays[label+'_anisotropic_stress']
        error=float(np.max(abs(np.trace(tensor,axis1=-2,axis2=-1)))/max(float(np.max(abs(tensor))),1e-300))
        check(label+': exported stress is tracefree',error<1e-13,max_envelope_error=error)
    check('Folded homogeneous channels kept',sum(row['homogeneous'] for row in configurations)==3)
    np.savez_compressed(folder/'source-packets.npz',**arrays,requested_scale=scales,conformal_time=times,
        masses_mpc_inverse=masses,configurations=np.array([[row['p_mpc_inverse'],row['q_mpc_inverse'],row['cosine'],row['K_mpc_inverse']] for row in configurations]))
    snapshots=[]
    for config_index,configuration in enumerate(configurations):
        for target_scale in [1e-6,.0002,.000225,.00025,.000265]:
            index=int(np.argmin(abs(scales-target_scale)))
            row=dict(configuration=configuration,scale=float(scales[index]))
            row['heavy_KG_temporal']=float(arrays['heavy_KG_temporal'][config_index,index])
            row['heavy_KG_spatial']=float(arrays['heavy_KG_spatial'][config_index,index])
            row['heavy_energy_quadratic']=float(arrays['heavy_E_quadratic'][config_index,index])
            row['heavy_stress_eigenvalues']=np.linalg.eigvalsh(arrays['heavy_anisotropic_stress'][config_index,index]).tolist()
            row['Einstein_volume_total_source']=float(arrays['Einstein_volume_total_source'][config_index,index])
            snapshots.append(row)
    write_json(folder/'snapshots.json',snapshots)
    inputs.extend([NATIVE/'fortran/equations.f90',NATIVE/'fortran/camb_python.f90',NATIVE/'fortran/MTSTwoField.f90',NATIVE/'camb/cambdll.dll'])
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,configurations=configurations,
        native_modes=wanted,field_sectors=labels,masses_mpc_inverse=masses,baryon_fraction_in_cdm_baryons=baryon_fraction,
        scale_range=[float(scales[0]),float(scales[-1])],time_samples=len(scales),native_scale_max_relative_error=native_scale_error,
        ordered_kernel_normalization='Per squared native primordial transfer amplitude; not multiplied by primordial power or real-cosine degeneracy factors.',
        units=dict(KG='Mpc^-2',E_P_anisotropy='8piG times physical stress: Mpc^-2',j_covariant='Mpc^-2',Einstein_volume='Mpc^-2'),
        source_channels_retained=['independent S2 and field2 coupled operators','ordinary species E2+3P2','second-order shear and Einstein constraints'],
        unspecified_channels_set_to_zero=False,full_nonlinear_solution=False,
        raw_transfer_standard_columns_have_float32_precision=True,finite_wave_vertices_do_not_use_noisy_finite_differences=True),__file__,inputs)
    print(json.dumps(dict(configurations=len(configurations),times=len(scales),checks=len(checks),max_trace_error=trace_error)),flush=True)


if __name__=='__main__':
    main()
