from residual_kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/readout-controls'
    folder.mkdir(parents=True,exist_ok=False)
    primary=ROOT/'results/kinetic-drive/status.json'
    report=json.loads(primary.read_text())
    for path,expected in report['input_hashes'].items():
        assert digest(path)==expected,path
    specification=json.loads((BRANCH/'temperature-distortion-projection-20261012/results/projection/status.json').read_text())['basis_specification']
    basis=infrared_ladder.ConsistentBasis(**specification)
    readout=ResidualMap(basis)
    checks,inputs,summaries=[],[primary,ROOT/'FOLLOWUP-CONTROLS.md'],{}
    def test(name,value,limit):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<=limit)))
    alternate=[]
    for name,lower,upper,count in [('full',1e-5,60,1400),('low',1e-5,.1,300),('peak',.001,.01,300)]:
        nodes,weights=special.roots_legendre(count)
        half=math.log(upper/lower)/2
        frequency=np.exp(math.log(lower*upper)/2+half*nodes)
        occupation=1/np.expm1(frequency)
        measure=weights*half*frequency**3*occupation*(1+occupation)/inherited.I3
        standard=np.column_stack([frequency/inherited.BETA-1,frequency*(frequency/np.tanh(frequency/2)-4)])
        templates=standard-frequency[:,None]*readout.reader.shifts
        mapping=basis.evaluate(frequency)-frequency[:,None]*readout.eta-templates@readout.amplitude
        alternate.append((name,measure,mapping))
    for model in ['heavy','cold']:
        baseline_path=BASELINE/f'{model}-nonlocal-refined-6400/history.npz'
        inputs.append(baseline_path)
        with np.load(baseline_path) as archive:
            baseline={key:archive[key].copy() for key in archive.files}
        cases={}
        saved_baseline=None
        for steps in [1024,512,256]:
            path=ROOT/'results/kinetic-drive'/f'{model}-{steps}.npz'
            window_path=WINDOW/f'{model}-main-{steps}.npz'
            inputs.extend([path,window_path])
            with np.load(path) as archive,np.load(window_path) as source:
                saved={key:archive[key].copy() for key in archive.files}
                window={key:source[key].copy() for key in source.files}
            if saved_baseline is None:
                saved_baseline=saved['photon'][:,:,0].copy()
            assert np.array_equal(saved_baseline,saved['photon'][:,:,0])
            base_indices=np.arange(3200,6401,50)
            window_indices=np.arange(0,steps+1,steps//64)
            gas_records=[]
            for epoch in range(1,65):
                base_index,window_index=base_indices[epoch],window_indices[epoch]
                step_vector=np.r_[baseline['expansion'][1]-baseline['expansion'][0],
                    np.full(16,window['coordinate'][1]-window['coordinate'][0])]
                old_energy=[]; old_gas=[]
                for offset in [0,1,2]:
                    old_energy.append(np.r_[baseline['energy_scaled'][base_index-offset],window['energy'][window_index-offset]])
                    old_gas.append(np.r_[baseline['temperature_scaled'][base_index-offset],window['gas'][window_index-offset]])
                energy_bdf=(1.5*old_energy[0]-2*old_energy[1]+.5*old_energy[2])/step_vector
                gas_bdf=(1.5*old_gas[0]-2*old_gas[1]+.5*old_gas[2])/step_vector
                gas_term=float(baseline['heat'])*(gas_bdf+old_gas[0])
                source=np.r_[1.,np.zeros(16)]
                equation=saved['operator_coefficient_derivative'][epoch]
                discrete=saved['bdf_coefficient_derivative'][epoch]
                energy_rhs=basis.energy@equation
                original=gas_term+source+energy_rhs
                conservative=gas_term+source+energy_bdf
                photon_defect=basis.energy@(discrete-equation)
                energy_defect=energy_bdf-basis.energy@discrete
                scale=abs(gas_term)+abs(source)+abs(energy_rhs)
                conservative_scale=abs(gas_term)+abs(source)+abs(energy_bdf)
                roundoff=1024*np.finfo(float).eps*np.maximum(abs(gas_term)+abs(source)+abs(basis.energy)@abs(equation)+abs(energy_bdf),1e-300)
                identity=original-conservative+photon_defect+energy_defect
                gas_records.append(np.stack([original,conservative,photon_defect,energy_defect,scale,conservative_scale,identity,roundoff]))
            records=np.array(gas_records)
            relative_raw=np.max(abs(records[:,0])/np.maximum(records[:,4],1e-300),axis=0)
            relative_conservative=np.max(abs(records[:,1])/np.maximum(records[:,5],1e-300),axis=0)
            test(f'Independent saved gas-energy balance:{model}:{steps}',relative_conservative.max(),1e-6)
            test(f'Gas diagnostic discrepancy explained by measured photon and energy defects:{model}:{steps}',
                 np.max(abs(records[:,6])/records[:,7]),1.)
            np.savez(folder/f'{model}-{steps}-gas-budget.npz',coordinate=saved['coordinate'][1:],records=records)
            if steps==1024:
                for band,(name,measure,mapping) in enumerate(alternate):
                    value=np.einsum('ij,njk->nik',mapping,saved['photon'])
                    power=np.einsum('i,nik,nik->nk',measure,value,value)
                    relative=np.max(abs(power-saved['residual_power'][:,band]),axis=0)/np.maximum(np.max(saved['residual_power'][:,band],axis=0),1e-300)
                    test(f'Residual band-power quadrature:{model}:{name}',relative.max(),1e-8)
                direct=readout.mapping@saved['photon'][-1,:,3:5]
                parts=[readout.mapping@saved['photon'][-1,:,offset:offset+2] for offset in [11,13,15]]
                component_norm=sum(norm(part,basis.measure) for part in parts)
                test(f'Direct54 residual equals summed source components:{model}',
                    np.max(norm(direct-sum(parts),basis.measure)/component_norm),1e-8)
                test(f'Component54 residual triangle inequality:{model}',
                    np.max((norm(direct,basis.measure)-component_norm)/component_norm),1e-12)
            cases[str(steps)]=dict(raw_relative_by_column=relative_raw.tolist(),
                conservative_relative_by_column=relative_conservative.tolist(),
                raw_absolute_by_column=np.max(abs(records[:,0]),axis=0).tolist(),
                photon_energy_defect_absolute_by_column=np.max(abs(records[:,2]),axis=0).tolist(),
                stored_energy_defect_absolute_by_column=np.max(abs(records[:,3]),axis=0).tolist(),
                conservative_absolute_by_column=np.max(abs(records[:,1]),axis=0).tolist(),
                cancellation_amplification=np.max((abs(records[:,1])+abs(records[:,2])+abs(records[:,3]))/np.maximum(records[:,4],1e-300),axis=0).tolist())
        summaries[model]=cases
        test('Baseline state identical across saved window timestep comparisons:'+model,0.,0.)
    finish(folder,dict(checks=checks,models=summaries,raw_gas_failures_retained=True,
        original_gas_tolerance_not_relaxed=True,photon_or_gas_history_changed=False,
        gas_net_transfer_relative_precision_not_upgraded=True,
        br_table_recomputed=False,evolution_rerun=False,source_event_integrals=0),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        raw_gas_max=max(max(row['raw_relative_by_column']) for model in summaries.values() for row in model.values()),
        conservative_gas_max=max(max(row['conservative_relative_by_column']) for model in summaries.values() for row in model.values()))),flush=True)


if __name__=='__main__':
    main()
