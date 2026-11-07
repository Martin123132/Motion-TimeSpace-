from three_quarter_history_common import *
from evaluate_stage139_feedback import expand_source
from propagate_matched_feedback import solve_response
import time


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/block-source-error'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    bank_path=ROOT/'results/coefficients/bank.npz'
    bank=read_npz(bank_path)
    checks,rows,inputs=[],{},[bank_path,bank_path.parent/'status.json',*ladder.inputs]
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for window in [20,40]:
            name=f'{model}-m{window}'
            current_folder=ROOT/'results'/f'feedback-{name}'
            previous_folder=PARENT/'results'/f'feedback-{name}'
            paths=[current_folder/'physical-source.npz',current_folder/'cubic-source.npz',
                previous_folder/'physical-source.npz',previous_folder/'cubic-source.npz',
                current_folder/'continuation-response.npz',previous_folder/'physical-response.npz']
            physical,cubic,previous_physical,previous_cubic,extension,reference=map(read_npz,paths)
            coordinate=physical['coordinate']
            assert np.array_equal(coordinate,cubic['coordinate'])
            old_physical=expand_source(previous_physical,coordinate)
            old_cubic=expand_source(previous_cubic,coordinate)
            forcing=(cubic['source']-physical['source'])-(old_cubic['source']-old_physical['source'])
            positions=np.searchsorted(coordinate,bank['coordinate'][1:])
            assert np.array_equal(coordinate[positions],bank['coordinate'][1:])
            outside=np.ones(len(coordinate),dtype=bool)
            outside[positions]=False
            assert not np.count_nonzero(forcing[outside])
            assert not np.count_nonzero(forcing[:,1:])
            checks.append(dict(name='Only new-block Compton discrepancy:'+name,passed=True))
            packet=dict(coordinate=coordinate,source=forcing)
            np.savez_compressed(folder/(name+'-source.npz'),**packet)
            solution,errors=solve_response(model,packet,2048,ladder,emission,background)
            np.savez_compressed(folder/(name+'-response.npz'),
                **{key:value for key,value in solution.items() if key!='photon'},
                photon_final=solution['photon'][-1],integration_steps=2048)
            checks.extend(check('Response:block-source-error:'+name+':'+key,value,1. if key=='energy_spectrum' else 1e-7)
                for key,value in errors.items())
            gas=solution['gas'][:,:3]
            signal=extension['gas'][:,:3]
            peak=np.max(abs(signal),axis=0)
            relative_peak=np.max(abs(gas),axis=0)/np.maximum(peak,1e-300)
            relative_endpoint=abs(gas[-1])/np.maximum(abs(signal[-1]),1e-300)
            near_zero=abs(signal[-1])<1e-6*peak
            relative_previous=abs(gas[-1])/np.maximum(abs(reference['gas'][-1,:3]),1e-300)
            for metric,values in [('peak',relative_peak),('endpoint',relative_endpoint)]:
                checks.extend(check('Sensitivity1percent:block-source-error:'+name+':'+metric+':'+column,value,.01)
                    for column,value in zip(['baseline','join1','join2'],values))
            rows[name]=dict(relative_peak_to_extension=relative_peak.tolist(),
                relative_endpoint_to_extension=relative_endpoint.tolist(),
                relative_endpoint_to_previous_correction=relative_previous.tolist(),
                extension_endpoint_near_zero=near_zero.tolist(),gas_endpoint=gas[-1].tolist(),
                extension_gas_endpoint=signal[-1].tolist(),response_errors=errors)
            inputs.extend([*paths,current_folder/'status.json',previous_folder/'status.json'])
            print(json.dumps(dict(case=name,relative_to_extension=relative_endpoint.tolist())),flush=True)
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Response:','Sensitivity1percent:')))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,response_steps=2048,
        discrepancy_is_new_block_only=True,rigorous_full_error_bound=False,
        frequency_grid_changed=False,inner_evolution_rerun=False,
        seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
