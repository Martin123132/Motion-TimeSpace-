from mixed_nodes import *
from compare_source_vectors import dual_norm
from inspect_coupled_response import response, NonlocalEmission, infrared_ladder


def main():
    modest()
    folder=ROOT/'results/mixed-budget'
    folder.mkdir(parents=True,exist_ok=False)
    fine_path=PARENT/'results/combined-source/source.npz'
    coarse_path=ROOT/'results/coarse-source/source.npz'
    ledger_path=PARENT/'results/radial-budget/responses.npz'
    previous_status_path=PARENT/'results/radial-budget/status.json'
    fine,coarse,ledger=[dict(np.load(path)) for path in [fine_path,coarse_path,ledger_path]]
    previous_status=json.loads(previous_status_path.read_text())
    spectra=Spectra(.5)
    mass=spectra.basis.mass
    assert np.array_equal(mass,fine['mass']) and np.array_equal(coarse['mass'],fine['mass'])
    previous={key.removeprefix('delta-'):value for key,value in ledger.items() if key.startswith('delta-')}
    replacements={key:fine[key]-coarse[key] for key in ['difference','virtual','state']}
    updated,mixed=replace_incoming(previous,replacements)
    denominator=dual_norm(fine['remainder'][1:-1],mass)
    assert np.min(denominator)>0
    def source_norm(value):
        return dual_norm(value[1:-1],mass)/denominator
    components={key:source_norm(value) for key,value in updated.items()}
    old_components={key:source_norm(value) for key,value in previous.items()}
    mixed_components={key:source_norm(value) for key,value in mixed.items()}
    budget,old_budget,mixed_budget=sum(components.values()),sum(old_components.values()),sum(mixed_components.values())
    frequency_budget=sum(components['incoming-'+key] for key in replacements)
    coherent=source_norm(sum(mixed.values()))
    checks=[
        dict(name='Updated incoming-frequency component-sum within1percent on refined grid',value=float(frequency_budget.max()),passed=bool(frequency_budget.max()<.01)),
        dict(name='Updated total observed component-sum within1percent',value=float(budget.max()),passed=bool(budget.max()<.01)),
        dict(name='Old source ledger reproduced without change',passed=bool(np.allclose(old_budget,previous_status['source_budget'],rtol=1e-12,atol=1e-14))),
        dict(name='No double counting:old and updated ledger have identical unique keys',passed=set(updated)==set(previous)),
        dict(name='Source budget change satisfies mixed-increment triangle bound',
            passed=bool(np.all(abs(budget-old_budget)<=mixed_budget+1e-12)))
    ]
    old_paths=[OUTER/'runs'/f's{order}-h3-g2-2-4/source.npz' for order in [3,4]]
    old=[dict(np.load(path)) for path in old_paths]
    identity_rows={}
    for key in replacements:
        alternative=(fine[key]-old[1][key])-(coarse[key]-old[0][key])
        error=source_norm(alternative-mixed[key])
        identity_rows[key]=error.tolist()
        checks.append(dict(name='Actual four-corner source identity:'+key,value=float(error.max()),passed=bool(error.max()<1e-10)))
        checks.append(dict(name='Component source triangle bound:'+key,
            passed=bool(np.all(components['incoming-'+key]<=old_components['incoming-'+key]+mixed_components[key]+1e-12))))
    arrays={'remainder':fine['remainder'],**{'delta-'+key:value for key,value in updated.items()},
        **{'old-delta-'+key:value for key,value in previous.items()},**{'mixed-'+key:value for key,value in mixed.items()}}
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    dependencies,response_rows=[],[]
    for model_index,model in enumerate(['heavy','cold']):
        background=thermal_wave.thermal.ThermalBackground(model)
        local=background.at(spectra.coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        selection=slice(2*model_index,2*model_index+2)
        for duration in [1e-3,1e-2]:
            solved,gases={},{}
            probes={'fine':fine['remainder'],**updated,
                **{'old-incoming-'+key:previous['incoming-'+key] for key in replacements},
                **{'mixed-'+key:value for key,value in mixed.items()}}
            for label,value in probes.items():
                photon,gas,metrics=response(ladder.basis,stiffness,rate,heat,value[1:-1,selection],value[-1,selection],duration)
                name=f'{model}-{duration}-{label}'
                arrays[name],arrays[name+'-gas']=photon,gas
                solved[label],gases[label]=photon,gas
                checks.append(dict(name='Original coupled equations and energy/work balance:'+name,
                    passed=bool(metrics['photon_equation_relative']<1e-7 and metrics['gas_equation_absolute']<1e-8
                        and metrics['energy_work_balance_absolute']<1e-14),**metrics))
            def photon_norm(value):
                return np.sqrt(np.maximum(np.sum(value*(mass@value),axis=0),0.))
            photon_scale,gas_scale=photon_norm(solved['fine']),abs(gases['fine'])
            assert np.min(photon_scale)>0 and np.min(gas_scale)>0
            photon_components={key:photon_norm(solved[key])/photon_scale for key in updated}
            gas_components={key:abs(gases[key])/gas_scale for key in updated}
            old_photon_components={key:photon_norm(solved['old-'+key] if key in ['incoming-'+part for part in replacements] else solved[key])/photon_scale for key in updated}
            old_gas_components={key:abs(gases['old-'+key] if key in ['incoming-'+part for part in replacements] else gases[key])/gas_scale for key in updated}
            mixed_photon={key:photon_norm(solved['mixed-'+key])/photon_scale for key in replacements}
            mixed_gas={key:abs(gases['mixed-'+key])/gas_scale for key in replacements}
            photon_budget,gas_budget=sum(photon_components.values()),sum(gas_components.values())
            old_photon_budget,old_gas_budget=sum(old_photon_components.values()),sum(old_gas_components.values())
            mixed_photon_budget,mixed_gas_budget=sum(mixed_photon.values()),sum(mixed_gas.values())
            expected=next(row for row in previous_status['response_rows'] if row['model']==model and row['duration']==duration)
            checks.append(dict(name=f'Old response ledger reproduced:{model}-{duration}',
                passed=bool(np.allclose(old_photon_budget,expected['photon_budget'],rtol=1e-11,atol=1e-14)
                    and np.allclose(old_gas_budget,expected['gas_budget'],rtol=1e-11,atol=1e-14))))
            for key in replacements:
                photon_error=photon_norm(solved['incoming-'+key]-solved['old-incoming-'+key]-solved['mixed-'+key])/photon_scale
                gas_error=abs(gases['incoming-'+key]-gases['old-incoming-'+key]-gases['mixed-'+key])/gas_scale
                checks.append(dict(name=f'Original response preserves four-corner identity:{model}-{duration}-{key}',
                    photon_relative=float(photon_error.max()),gas_relative=float(gas_error.max()),
                    passed=bool(photon_error.max()<1e-9 and gas_error.max()<1e-9)))
            for label,value,old_value,mixed_value in [('photon',photon_budget,old_photon_budget,mixed_photon_budget),
                ('gas',gas_budget,old_gas_budget,mixed_gas_budget)]:
                checks.append(dict(name=f'Updated total observed {label} budget within1percent:{model}-{duration}',
                    value=float(value.max()),passed=bool(value.max()<.01)))
                checks.append(dict(name=f'{label} budget change obeys mixed triangle bound:{model}-{duration}',
                    passed=bool(np.all(abs(value-old_value)<=mixed_value+1e-12))))
            response_rows.append(dict(model=model,duration=duration,photon_budget=photon_budget.tolist(),gas_budget=gas_budget.tolist(),
                old_photon_budget=old_photon_budget.tolist(),old_gas_budget=old_gas_budget.tolist(),
                mixed_photon_budget=mixed_photon_budget.tolist(),mixed_gas_budget=mixed_gas_budget.tolist(),
                photon_components={key:value.tolist() for key,value in photon_components.items()},
                gas_components={key:value.tolist() for key,value in gas_components.items()}))
        dependencies.extend([*emission.inputs,background.parent.source,background.native_constants])
    np.savez(folder/'responses.npz',**arrays)
    finish(folder,dict(checks=checks,source_budget=budget.tolist(),old_source_budget=old_budget.tolist(),
        refined_incoming_budget=frequency_budget.tolist(),mixed_budget=mixed_budget.tolist(),coherent_mixed_change=coherent.tolist(),
        source_components={key:value.tolist() for key,value in components.items()},
        old_source_components={key:value.tolist() for key,value in old_components.items()},
        mixed_source_components={key:value.tolist() for key,value in mixed_components.items()},
        four_corner_relative_residuals=identity_rows,response_rows=response_rows,
        combined_observed_budget_passed=all(row['passed'] for row in checks),
        composite_frequency_geometry_increment_computed=True,isolated_single_axis_mixed_derivative=False,
        fine_source_unchanged=True,rigorous_continuum_error_bound=False,all_dimension_remainder_gate_closed=False,
        new_parent_history=False,full_parent_feedback_applied=False),__file__,
        [fine_path,coarse_path,ledger_path,previous_status_path,*old_paths,ROOT/'mixed_nodes.py',
         *spectra.inputs,*ladder.inputs,*dependencies])
    print(json.dumps(dict(source_budget=budget.tolist(),old_source_budget=old_budget.tolist(),mixed_budget=mixed_budget.tolist(),
        refined_incoming_budget=frequency_budget.tolist(),coherent_mixed_change=coherent.tolist(),
        response_summary=[dict(model=row['model'],duration=row['duration'],photon=max(row['photon_budget']),
            gas=max(row['gas_budget']),mixed_photon=max(row['mixed_photon_budget']),mixed_gas=max(row['mixed_gas_budget'])) for row in response_rows],
        failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
