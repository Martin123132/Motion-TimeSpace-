from matched_feedback_common import *


def main():
    modest()
    folder=ROOT/'results/energy-accounting'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,inputs,metrics=[],[*ladder.inputs],{}
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        source_path=ROOT/'results/sources-fine-q32-m40'/(model+'.npz')
        inputs.append(source_path)
        with np.load(source_path) as archive:
            forcing=interpolate.interp1d(archive['coordinate'],archive['source'],axis=0,bounds_error=True)
        for steps in [512,1024]:
            path=ROOT/'results'/f'response-fine-q32-m40-n{steps}'/(model+'.npz')
            inputs.append(path)
            with np.load(path) as archive:
                photon,gas,energy=[archive[key].copy() for key in ['photon','gas','energy']]
                times=archive['coordinate'].copy()
            step=times[1]-times[0]
            identity_max,bound_max,gas_max=0.,0.,0.
            for index in range(steps//64,steps+1,steps//64):
                position=times[index]
                local=background.at(float(position))
                rate=local['coefficient']/local['thermal_parameter']
                stiffness=ladder.at(local['thermal_parameter'],0)[:96,:96]-emission.at(local['thermal_parameter'],'dcbr')
                pieces=forcing(position)
                external=np.column_stack([pieces.sum(axis=0),*pieces])
                departure=photon[index]-basis.temperature[:,None]*gas[index]
                physical=stiffness@departure+external
                derivative=(1.5*photon[index]-2*photon[index-1]+.5*photon[index-2])/step
                gas_derivative=(1.5*gas[index]-2*gas[index-1]+.5*gas[index-2])/step
                energy_derivative=(1.5*energy[index]-2*energy[index-1]+.5*energy[index-2])/step
                photon_residual=basis.mass@derivative-rate*physical
                gas_residual=background.chi*(gas_derivative+gas[index])+rate*basis.temperature@physical
                spectral_defect=basis.energy@derivative-energy_derivative
                independent_balance=energy_derivative+background.chi*(gas_derivative+gas[index])
                predicted=independent_balance+spectral_defect-basis.temperature@photon_residual
                operands=abs(basis.temperature)@(abs(basis.mass)@abs(derivative)+abs(rate)*(abs(stiffness)@abs(departure)+abs(external)))
                allowance=2048*np.finfo(float).eps*np.maximum(operands+abs(energy_derivative)+background.chi*(abs(gas_derivative)+abs(gas[index])),1e-300)
                identity_max=max(identity_max,float(np.max(abs(gas_residual-predicted)/allowance)))
                explained=abs(independent_balance)+abs(spectral_defect)+abs(basis.temperature)@abs(photon_residual)+allowance
                bound_max=max(bound_max,float(np.max(abs(gas_residual)/np.maximum(explained,1e-300))))
                gas_max=max(gas_max,float(abs(gas_residual).max()))
            label=model+':'+str(steps)
            checks.extend([
                dict(name='Gas residual decomposes into saved energy and photon residual:'+label,value=identity_max,limit=1.,passed=identity_max<=1),
                dict(name='Absolute gas residual within independent operand bound:'+label,value=bound_max,limit=1.,passed=bound_max<=1)])
            metrics[label]=dict(maximum_absolute_gas_residual=gas_max,identity_allowance_ratio=identity_max,bound_ratio=bound_max)
    finish(folder,dict(checks=checks,metrics=metrics,raw_gas_relative_gate_closed=False,
        original_failures_retained=True,independent_saved_energy_used=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,metrics=metrics)),flush=True)


if __name__=='__main__':
    main()
