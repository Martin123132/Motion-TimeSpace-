from stage163_common import *
from stable_moments import StableMoments


def compensated(values):
    array=np.asarray(values)
    flat=array.reshape(array.shape[0],-1)
    return np.asarray([math.fsum(flat[:,column]) for column in range(flat.shape[1])]).reshape(array.shape[1:])


class CompensatedReal(StableMoments):
    def real(self,parameters,angular=3,radial=32,floor=1e-6,rule=None):
        if rule is None:
            rule=PanelRule(.5)
        jump,product=self.born_data(parameters)
        spontaneous,thermal,logarithm=[],[],[]
        maximum_null=0.
        for direction,angular_weight in weak.source.angular_nodes(angular):
            doppler=weak.source.dot(parameters['bath'],np.r_[1.,direction])
            local_temperature=parameters['temperature']/doppler
            emission_upper=weak.source.bath_ordered_upper(parameters,direction)
            absorption_upper=parameters['lab_energy']/doppler
            lower=floor*local_temperature
            assert lower<min(emission_upper,absorption_upper)
            pole=self.poles(parameters,direction)
            values,weights=rule(radial,lower,emission_upper)
            density,products,jumps=self.event_products(parameters,values,direction)
            residual=density[:,None,None]*products-pole/values[:,None,None]*product
            spontaneous.append(.5*angular_weight*compensated(weights[:,None,None]*residual))
            maximum_null=max(maximum_null,float(np.max(abs(jumps[:,0]+jumps[:,-1]))))
            logarithm.append(.5*angular_weight*pole*math.log(2*emission_upper)*product)
            tail_upper=max(60*local_temperature,emission_upper,absorption_upper)
            boundaries=[lower,emission_upper,absorption_upper,tail_upper]
            boundaries+=[scale*local_temperature for scale in [.1,.5,1,2,5,10,20,40]
                if lower<scale*local_temperature<tail_upper]
            boundaries=sorted(set(boundaries))
            for left,right in zip(boundaries[:-1],boundaries[1:]):
                values,weights=rule(radial,left,right)
                occupation=1/np.expm1(values/local_temperature)
                terms=[-2*pole/values[:,None,None]*product]
                for sign,upper in [(1,emission_upper),(-1,absorption_upper)]:
                    if right<=upper*(1+1e-14):
                        density,products,jumps=self.event_products(parameters,sign*values,direction)
                        terms.append(density[:,None,None]*products)
                        maximum_null=max(maximum_null,float(np.max(abs(jumps[:,0]+jumps[:,-1]))))
                residual=compensated(terms)
                thermal.append(.5*angular_weight*compensated((weights*occupation)[:,None,None]*residual))
        pieces=[compensated(values) for values in [spontaneous,thermal,logarithm]]
        return dict(total=compensated(pieces),spontaneous=pieces[0],thermal=pieces[1],
            logarithm=pieces[2],event_energy_null=maximum_null)


def main():
    modest()
    folder=ROOT/'results/compensated-probe'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    inputs=[ROOT/'results/preflight/status.json']
    checks,records=[],{}
    for endpoint in ENDPOINTS:
        theta=proof['contexts'][endpoint][0]['theta']
        ranked=[]
        for order in [5,6]:
            for node in integration_nodes(theta,order):
                path=moment_path(endpoint,order,node['index'])
                event=read_npz(path)
                defect=float(event['weight'])*max(abs(event['difference'][0]+event['difference'][-1]))
                ranked.append((defect,order,node,path))
                inputs.append(path)
        bundle=EpochBundle(ENDPOINTS[endpoint])
        model=CompensatedReal(bundle)
        inputs.extend(bundle.inputs)
        for defect,order,node,path in sorted(ranked,key=lambda item:item[0],reverse=True)[:4]:
            old=read_npz(path)['difference']
            parameters,weight=parameters_and_weight(theta,node)
            started=time.monotonic()
            result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
            new=result['total']
            tag=endpoint+f'-order{order}-node'+str(node['index'])
            scale=np.maximum(abs(old[0]),1e-300)
            old_pair=abs(old[0]+old[-1])/scale
            new_pair=abs(new[0]+new[-1])/scale
            change=np.max(abs(new-old),axis=0)/np.maximum(np.max(abs(old),axis=0),1e-300)
            test(checks,'Same physical integral up to summation rounding:'+tag,float(max(change)),1e-10)
            test(checks,'Unchanged independent event absolute exchange:'+tag,result['event_energy_null'],1e-10)
            records[tag]=dict(old_pair=old_pair.tolist(),new_pair=new_pair.tolist(),
                old_weighted_defect=defect,new_weighted_defect=weight*float(max(abs(new[0]+new[-1]))),
                improvement=(old_pair/np.maximum(new_pair,1e-300)).tolist(),
                relative_source_change=change.tolist(),seconds=time.monotonic()-started)
            np.savez_compressed(folder/(tag+'.npz'),old=old,new=new,weight=weight,identity=json.dumps(node,sort_keys=True))
            print(json.dumps(dict(case=tag,record=records[tag])),flush=True)
    finish(folder,dict(checks=checks,records=records,probes=8,full_compensated_source_computed=False,
        gas_equals_minus_photon_enforced=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
