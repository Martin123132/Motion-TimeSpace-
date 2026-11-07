from response_sites_common import *
from propagate_matched_feedback import solve_response
import time


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/site-attribution'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows=[],[]
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for upper in [.04,.02]:
            label=int(upper*1000)
            source_folder=ROOT/'results'/f'sites-{model}-m{label}'
            status=local_packet(source_folder)
            inputs.append(source_folder/'status.json')
            sources={}
            responses={}
            for variant in ['assembled','direct']:
                for representation in ['control','sites32']:
                    key=variant+'-'+representation
                    source_path=source_folder/(key+'-source.npz')
                    response_path=source_folder/(key+'-response.npz')
                    inputs.extend([source_path,response_path])
                    sources[key]=read_npz(source_path)
                    responses[key]=read_npz(response_path)
            coordinate=sources['direct-sites32']['coordinate']
            direct=sources['direct-sites32']['source']-sources['direct-control']['source']
            assembled=sources['assembled-sites32']['source']-sources['assembled-control']['source']
            start,end=coordinate[[0,-1]]
            first_coordinate=float(start+(end-start)/2048)
            first_index=int(np.flatnonzero(coordinate==first_coordinate)[0])
            first=np.zeros_like(direct)
            first[first_index]=direct[first_index]
            remaining=direct-first
            operator=direct-assembled
            checks.append(dict(name=f'Exact first/rest source split:{model}:{upper}',passed=np.array_equal(first+remaining,direct)))
            checks.append(dict(name=f'Operator change is Compton-only:{model}:{upper}',passed=not np.count_nonzero(operator[:,1:])))
            assert np.count_nonzero(np.any(direct!=0,axis=(1,2,3)))==16
            propagated={}
            for split,values in [('first',first),('remaining',remaining),('operator',operator)]:
                source=dict(coordinate=coordinate,source=values)
                solution,errors=solve_response(model,source,2048,ladder,emission,background)
                np.savez_compressed(folder/f'{model}-m{label}-{split}.npz',**source,
                    response_coordinate=solution['coordinate'],gas=solution['gas'],energy=solution['energy'],
                    work=solution['work'],number=solution['number'],photon_final=solution['photon'][-1])
                checks.extend(check(f'Response:attribution:{model}:{upper}:{split}:'+name,value,
                    1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
                propagated[split]=solution
            delta_gas=responses['direct-sites32']['gas']-responses['direct-control']['gas']
            difference=delta_gas-propagated['first']['gas']-propagated['remaining']['gas']
            scale=np.maximum((abs(responses['direct-sites32']['gas'])+abs(responses['direct-control']['gas'])
                +abs(propagated['first']['gas'])+abs(propagated['remaining']['gas'])).max(axis=0),1e-300)
            closure=float(np.max(abs(difference)/scale))
            checks.append(check(f'First/rest reproduce direct gas increment:{model}:{upper}',closure,1e-7))
            assembled_gas=responses['assembled-sites32']['gas']-responses['assembled-control']['gas']
            operator_difference=delta_gas-assembled_gas-propagated['operator']['gas']
            operator_scale=np.maximum((abs(responses['direct-sites32']['gas'])+abs(responses['direct-control']['gas'])
                +abs(responses['assembled-sites32']['gas'])+abs(responses['assembled-control']['gas'])
                +abs(propagated['operator']['gas'])).max(axis=0),1e-300)
            operator_closure=float(np.max(abs(operator_difference)/operator_scale))
            checks.append(check(f'Operator increment reproduces paired gas difference:{model}:{upper}',operator_closure,1e-7))
            checks.append(dict(name=f'No DC/BR gas in operator increment:{model}:{upper}',
                passed=not np.count_nonzero(propagated['operator']['gas'][:,6:])))
            checks.append(dict(name=f'No changed source outside first interval:{model}:{upper}',
                passed=not np.count_nonzero(direct[coordinate>=float(start+(end-start)/64)])))
            endpoint=delta_gas[-1,:3]
            first_endpoint=propagated['first']['gas'][-1,:3]
            remaining_endpoint=propagated['remaining']['gas'][-1,:3]
            operator_endpoint=propagated['operator']['gas'][-1,:3]
            rows.append(dict(model=model,upper=upper,direct_endpoint_increment=endpoint.tolist(),
                first_endpoint=first_endpoint.tolist(),remaining_endpoint=remaining_endpoint.tolist(),
                operator_endpoint=operator_endpoint.tolist(),
                first_signed_fraction=(first_endpoint/np.where(endpoint==0,np.inf,endpoint)).tolist(),
                operator_signed_fraction=(operator_endpoint/np.where(endpoint==0,np.inf,endpoint)).tolist(),
                first_rest_closure=closure,operator_closure=operator_closure,
                first_peak=abs(propagated['first']['gas'][:,:3]).max(axis=0).tolist(),
                remaining_peak=abs(propagated['remaining']['gas'][:,:3]).max(axis=0).tolist()))
            print(json.dumps(rows[-1]),flush=True)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,diagnostic_added_after_main_result=True,
        does_not_certify_time_integration=True,seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
