from response_time_common import *


SELECTED=[1,2,64,1024,2048,3072,3584,4095,4096]


def physical_residuals(response,source,ladder,emission,background):
    basis=ladder.basis
    step=(response['coordinate'][-1]-response['coordinate'][0])/4096
    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
    records=[]
    for index in SELECTED:
        alpha=(1. if index==1 else 1.5)/step
        history={}
        for name in ['photon','gas','work']:
            history[name]=(response[name][index-1] if index==1 else 2*response[name][index-1]-.5*response[name][index-2])/step
        photon,gas,work=[response[name][index] for name in ['photon','gas','work']]
        local=background.at(float(response['coordinate'][index]))
        theta,rate=local['thermal_parameter'],local['coefficient']/local['thermal_parameter']
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        pieces=forcing(float(response['coordinate'][index]))
        external=np.column_stack([pieces.sum(axis=0),*pieces])
        physical=stiffness@(photon-basis.temperature[:,None]*gas)+external
        photon_residual=basis.mass@(alpha*photon-history['photon'])-rate*physical
        photon_scale=np.maximum(np.linalg.norm(alpha*basis.mass@photon,axis=0)+
            np.linalg.norm(basis.mass@history['photon'],axis=0)+np.linalg.norm(rate*physical,axis=0),1e-300)
        gas_residual=background.chi*((alpha+1)*gas-history['gas'])+rate*basis.temperature@physical
        gas_scale=np.maximum(abs(background.chi*(alpha+1)*gas)+abs(background.chi*history['gas'])+
            abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
        work_residual=alpha*work-history['work']-background.chi*gas
        work_scale=np.maximum(abs(alpha*work)+abs(history['work'])+abs(background.chi*gas),1e-300)
        records.append(dict(step=index,photon=(np.linalg.norm(photon_residual,axis=0)/photon_scale).tolist(),
            gas=(abs(gas_residual)/gas_scale).tolist(),work=(abs(work_residual)/work_scale).tolist()))
    return records


def main():
    modest()
    folder=ROOT/'results/equation-audit'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    checks,rows,inputs=[],[],list(ladder.inputs)
    for upper in [.04,.02]:
        for model in ['heavy','cold']:
            response_path=ROOT/'results'/f'response-m{int(upper*1000)}-r4096'/(model+'-response.npz')
            source_path=PARENT/'results'/f'feedback-m{int(upper*1000)}-n10240'/(model+'-source.npz')
            local_packet(response_path.parent)
            local_packet(source_path.parent)
            background=thermal_wave.thermal.ThermalBackground(model)
            emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
            inputs.extend([response_path,response_path.parent/'status.json',source_path,
                source_path.parent/'status.json',*emission.inputs,background.parent.source,background.native_constants])
            records=physical_residuals(read_npz(response_path),read_npz(source_path),ladder,emission,background)
            maximum={key:float(np.max([row[key] for row in records])) for key in ['photon','gas','work']}
            checks.extend(check(f'{model}:m{int(upper*1000)}:Independent physical {name}',value,1e-7)
                for name,value in maximum.items())
            rows.append(dict(model=model,upper=upper,records=records,maximum=maximum))
    finish(folder,dict(checks=checks,rows=rows,selected_steps=SELECTED,
        physical_equations_checked=True,gas_gate_relaxed=False,not_arbitrary_precision=True),__file__,inputs)
    print(json.dumps(dict(rows=[dict(model=row['model'],upper=row['upper'],maximum=row['maximum']) for row in rows],
        failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
