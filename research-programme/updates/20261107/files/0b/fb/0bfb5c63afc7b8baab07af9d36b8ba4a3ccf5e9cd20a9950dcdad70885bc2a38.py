from __future__ import annotations

from onset_common import *


def main():
    modest()
    folder=ROOT/'results/resolved-comparison-valid'
    folder.mkdir(parents=True,exist_ok=False)
    grid_path=ROOT/'runs/heavy-fine/fluids.npz'
    model=Background('heavy',np.load(grid_path))
    solution=model.solve(math.log(2e-9),2e-11)
    old_source=model.source
    old=np.load(old_source)
    candidate={key:old[key].copy() for key in old.files}
    selected=(old['efold']>=math.log(2e-9))&(old['efold']<=FINAL)
    nodes=old['efold'][selected]
    names,values=physical(model,nodes,solution.sol(nodes))
    candidate['phi_s'][selected]=values[names.index('phi_s')]
    candidate['phidot_s'][selected]=np.exp(nodes)*values[names.index('dotphi_s')]
    candidate_path=folder/'early-slow-source-test-only.npz'
    np.savez_compressed(candidate_path,**candidate)
    query=np.unique(np.r_[np.linspace(math.log(1e-6),FINAL,181),np.log(np.linspace(.00018,.00026,1601))])
    query=query[query<=math.log(.00026)]
    scales=np.exp(query)
    derived_names,derived_values=physical(model,query,solution.sol(query))
    derived={name:derived_values[index] for index,name in enumerate(derived_names)}
    waves=np.array([.0001,.0002,.0004,.001,.03])
    names=camb.model.evolve_names
    rows=[]
    paths=[grid_path,old_source,candidate_path,ROOT/'results/native-comparison/heavy.npz']
    for label,source in [('original-dense',old_source),('corrected-early-slow',candidate_path)]:
        params=inherited.inherited.params_for(source)
        native=camb.get_background(params)
        native.Params.Accuracy.IntTolBoost=7
        times=native.conformal_time(1/scales-1,tol=1e-10)
        native_values=native.get_time_evolution(waves,times,vars=names,lAccuracyBoost=4)
        assert np.isfinite(native_values).all()
        assert np.all(native_values[:,:,names.index('a')]>0)
        assert np.max(abs(native_values[:,:,names.index('a')]/scales-1))<1e-6
        output=folder/(label+'.npz')
        np.savez_compressed(output,waves=waves,scales=scales,times=times,names=names,values=native_values,derived_names=derived_names,derived_values=derived_values)
        paths.append(output)
        for index,wave in enumerate(waves):
            eta=native_values[index,:,names.index('etak')]/wave
            zeta=-eta[0]/(1-wave**2*(derived['b'][0]-8*derived['s'][0])/6)
            for quantity,key,predicted in [
                ('cold','delta_cdm',-4*wave**2*zeta*derived['s']),
                ('photon','delta_photon',-16*wave**2*zeta*derived['s']/3),
                ('field_s','mts_dphi_s',4*wave**2*zeta*derived['f_s']),
                ('field_h','mts_dphi_h',4*wave**2*zeta*derived['f_h'])]:
                actual=native_values[index,:,names.index(key)]
                error=float(max(abs(actual-predicted))/max(max(abs(actual)),max(abs(predicted)),1e-90))
                rows.append(dict(source_variant=label,k_Mpc_inverse=float(wave),quantity=quantity,
                    envelope_relative_error=error,primary=bool(wave<=.0004),qualified=bool(error<.01)))
        print(json.dumps(dict(source_variant=label,rows=rows[-20:])),flush=True)
    early=nodes<math.log(.00025)
    actual_velocity=old['phidot_s'][selected]/np.exp(nodes)
    derived_velocity=values[derived_names.index('dotphi_s')]
    late=early&(nodes>math.log(.00005))
    previous=BRANCH/'radiation-and-slow-field-transfer-20261007/radiation_common.py'
    finish(folder,dict(rows=rows,original_slow_velocity_max_relative_error=float(max(abs(actual_velocity[late]/derived_velocity[late]-1))),
        corrected_primary_pass=all(row['qualified'] for row in rows if row['source_variant']=='corrected-early-slow' and row['primary']),
        candidate_table_scope='Early-slow-source comparison only. Original entries after a=0.000265 remain unchanged. Not a global repaired cosmology table; do not feed this splice to late predictions.',
        maximum_native_query_scale=float(max(scales)),old_library_and_tables_modified=False,
        diagnosed_sparse_response_interpolation=True,old_slow_atol=1e-13,source_precision_followup_required=True),__file__,paths+[previous])


if __name__=='__main__':
    main()
