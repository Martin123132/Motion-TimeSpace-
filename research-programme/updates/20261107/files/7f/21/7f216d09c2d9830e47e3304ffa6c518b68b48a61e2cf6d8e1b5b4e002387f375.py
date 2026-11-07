from residual_kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/interpretation'
    folder.mkdir(parents=True,exist_ok=False)
    raw_path=ROOT/'results/kinetic-drive/status.json'
    control_path=ROOT/'results/readout-controls/status.json'
    raw=json.loads(raw_path.read_text())
    controls=json.loads(control_path.read_text())
    assert controls['all_checks_passed']
    inputs=[raw_path,control_path]
    checks,summary=[],{}
    for model in ['heavy','cold']:
        path=ROOT/'results/kinetic-drive'/f'{model}-1024.npz'
        inputs.append(path)
        with np.load(path) as archive:
            saved={key:archive[key] for key in archive.files}
        power=saved['residual_power'][:,:,:3]
        rates=saved['residual_power_half_derivative_terms'][:,:,:,:,:3]
        net=rates.sum(axis=(2,3))
        operator_net=rates.sum(axis=3)
        self_term=rates[:,:,:,0].sum(axis=2)
        template_drive=rates[:,:,:,1:].sum(axis=(2,3))
        assert np.all(self_term[:,0]<=0)
        checks.append(dict(name='Independent drive+self equals total:'+model,
            passed=bool(np.max(abs(net-self_term-template_drive)/np.maximum(abs(self_term)+abs(template_drive),1e-300))<1e-12)))
        checks.append(dict(name='Both central joins have same qualitative history:'+model,
            passed=bool(np.array_equal(np.sign(net[:,:,1]),np.sign(net[:,:,2])))))
        derivative_flags=[]
        for column in range(3):
            derivative_flags.append({name:[dict(bracket=(saved['coordinate'][index:index+2]/math.log(10)).tolist(),
                from_sign=int(np.sign(net[index,band,column])),to_sign=int(np.sign(net[index+1,band,column])))
                for index in np.flatnonzero(np.sign(net[1:,band,column])!=np.sign(net[:-1,band,column]))]
                for band,name in enumerate(['full','low','peak'])})
        minimum_indices=np.argmin(power,axis=0)
        minimum_fraction=np.take_along_axis(power,minimum_indices[None,:,:],axis=0)[0]/power[0]
        summary[model]=dict(
            column_order=['baseline','correction_join1','correction_join2'],
            band_order=['full','low','peak'],
            residual_norm_final_over_start=np.sqrt(power[-1]/power[0]).tolist(),
            residual_power_final_over_start=(power[-1]/power[0]).tolist(),
            minimum_residual_power_over_start=minimum_fraction.tolist(),
            minimum_epoch_fraction=(saved['coordinate'][minimum_indices]/math.log(10)).tolist(),
            derivative_sign_change_brackets=derivative_flags,
            final_residual_power_relative_growth_per_u=(2*net[-1]/power[-1]).tolist(),
            endpoint_net_half_power_rate_by_operator=operator_net[-1].tolist(),
            endpoint_residual_self_half_power_rate=self_term[-1].tolist(),
            endpoint_template_drive_half_power_rate=template_drive[-1].tolist(),
            endpoint_net_to_total_rate_magnitude=(abs(net[-1])/np.sum(abs(rates[-1]),axis=(1,2))).tolist(),
            endpoint_half_power_rate_by_resolved_drive=rates[-1].sum(axis=1).tolist(),
            source54_residual_norm_budget=raw['models'][model]['source54_endpoint_residual_component_budget'],
            saved512_vs1024_residual_norm_comparison=raw['models'][model]['refinements']['512'],
            raw_gas_primary_relative=controls['models'][model]['1024']['raw_relative_by_column'][:3],
            independent_energy_gas_primary_relative=controls['models'][model]['1024']['conservative_relative_by_column'][:3])
    finish(folder,dict(checks=checks,models=summary,empirical_fit=False,no_new_history=True,
        low_frequency_residual_driven_and_damped=True,autonomous_exponential_decay_rejected_for_saved_interval=True,
        new_observation=False),__file__,inputs)
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    main()
