from stage163_common import *
from stable_moments import StableMoments
from probe_compensated_real import compensated


class CorrelatedSoft(StableMoments):
    def jumps(self,incoming,hard,soft,electron):
        left,right=super().jumps(incoming,hard,soft,electron)
        self.last_right=right
        return left,right

    def difference_product(self,parameters,soft,direction,born_left,born_right):
        density,products,left=self.event_products(parameters,soft,direction)
        right=self.last_right
        energy=parameters['energy']
        angular=1-parameters['cosine']
        mixed=1-parameters['hard_direction']@direction
        incident_soft=1-direction[2]
        initial_denominator=1+energy*angular
        denominator=initial_denominator-soft*mixed
        hard_shift=-soft*((1+energy*incident_soft)*initial_denominator-energy*mixed)/(initial_denominator*denominator)
        energy_shift=soft*(energy*(initial_denominator*(angular-incident_soft)+mixed)-soft*mixed*initial_denominator)/(initial_denominator*denominator)
        recoil0=np.array([0.,0.,energy])-parameters['hard']*parameters['hard_direction']
        recoil_shift=-hard_shift[:,None]*parameters['hard_direction']-soft[:,None]*direction
        recoil=recoil0+recoil_shift
        rest_shift=(2*(recoil_shift@recoil0)+np.sum(recoil_shift**2,axis=1))/(
            np.sqrt(1+np.sum(recoil**2,axis=1))+math.sqrt(1+recoil0@recoil0))
        transform=parameters['transform']
        photon_shift=(transform[0,0]*energy_shift-recoil_shift@transform[0,1:])/parameters['temperature']
        electron_shift=(transform[0,0]*rest_shift+recoil_shift@transform[0,1:])/parameters['temperature']
        delta=np.column_stack([photon_shift,np.sign(soft),electron_shift])
        difference=np.einsum('ni,nj->nij',delta,right)+np.einsum('i,nj->nij',born_left,right-born_right)
        return density,difference,left,delta

    def real(self,parameters,angular=4,radial=18,floor=1e-6,rule=None):
        if rule is None:
            rule=PanelRule(.5)
        born_left,born_right=self.born_jumps(parameters)
        product=np.outer(born_left,born_right)
        spontaneous,thermal,logarithm=[],[],[]
        maximum_null=maximum_shift_null=0.
        for direction,angular_weight in weak.source.angular_nodes(angular):
            doppler=weak.source.dot(parameters['bath'],np.r_[1.,direction])
            local_temperature=parameters['temperature']/doppler
            emission_upper=weak.source.bath_ordered_upper(parameters,direction)
            absorption_upper=parameters['lab_energy']/doppler
            lower=floor*local_temperature
            assert lower<min(emission_upper,absorption_upper)
            pole=self.poles(parameters,direction)
            values,weights=rule(radial,lower,emission_upper)
            density,difference,jumps,delta=self.difference_product(parameters,values,direction,born_left,born_right)
            residual=density[:,None,None]*difference+(density-pole/values)[:,None,None]*product
            spontaneous.append(.5*angular_weight*compensated(weights[:,None,None]*residual))
            maximum_null=max(maximum_null,float(np.max(abs(jumps[:,0]+jumps[:,-1]))))
            maximum_shift_null=max(maximum_shift_null,float(np.max(abs(delta[:,0]+delta[:,-1]))))
            logarithm.append(.5*angular_weight*pole*math.log(2*emission_upper)*product)
            tail_upper=max(60*local_temperature,emission_upper,absorption_upper)
            boundaries=[lower,emission_upper,absorption_upper,tail_upper]
            boundaries+=[scale*local_temperature for scale in [.1,.5,1,2,5,10,20,40]
                if lower<scale*local_temperature<tail_upper]
            boundaries=sorted(set(boundaries))
            for lower_panel,upper_panel in zip(boundaries[:-1],boundaries[1:]):
                values,weights=rule(radial,lower_panel,upper_panel)
                occupation=1/np.expm1(values/local_temperature)
                densities=[-2*pole/values]
                differences=[]
                for sign,upper in [(1,emission_upper),(-1,absorption_upper)]:
                    if upper_panel<=upper*(1+1e-14):
                        density,difference,jumps,delta=self.difference_product(parameters,sign*values,direction,born_left,born_right)
                        densities.append(density)
                        differences.append(density[:,None,None]*difference)
                        maximum_null=max(maximum_null,float(np.max(abs(jumps[:,0]+jumps[:,-1]))))
                        maximum_shift_null=max(maximum_shift_null,float(np.max(abs(delta[:,0]+delta[:,-1]))))
                residual=compensated(densities)[:,None,None]*product
                if differences:
                    residual+=compensated(differences)
                thermal.append(.5*angular_weight*compensated((weights*occupation)[:,None,None]*residual))
        pieces=[compensated(values) for values in [spontaneous,thermal,logarithm]]
        return dict(total=compensated(pieces),spontaneous=pieces[0],thermal=pieces[1],logarithm=pieces[2],
            event_energy_null=maximum_null,shift_energy_null=maximum_shift_null)


def main():
    modest()
    folder=ROOT/'results/correlated-soft-probe'
    folder.mkdir(parents=True,exist_ok=False)
    controls=verify_packet(ROOT/'results/compensated-probe')
    proof=verify_packet(ROOT/'results/preflight')
    checks,records=[],{}
    inputs=[ROOT/'results/compensated-probe/status.json',ROOT/'results/preflight/status.json',ROOT/'SOFT-SUBTRACTION-DERIVATION.md']
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        model=CorrelatedSoft(bundle)
        inputs.extend(bundle.inputs)
        theta=proof['contexts'][endpoint][0]['theta']
        for tag in controls['records']:
            if not tag.startswith(endpoint+'-'):
                continue
            prior_path=ROOT/'results/compensated-probe'/(tag+'.npz')
            prior=read_npz(prior_path)
            node=json.loads(str(prior['identity']))
            parameters,weight=parameters_and_weight(theta,node)
            started=time.monotonic()
            result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
            new=result['total']
            old=prior['old']
            scale=np.maximum(abs(old[0]),1e-300)
            old_pair=abs(old[0]+old[-1])/scale
            new_pair=abs(new[0]+new[-1])/scale
            change=np.max(abs(new-old),axis=0)/np.maximum(np.max(abs(old),axis=0),1e-300)
            test(checks,'Equivalent soft-subtracted source:'+tag,float(max(change)),1e-10)
            test(checks,'Independent soft-shift photon/gas:'+tag,result['shift_energy_null'],1e-10)
            test(checks,'Independent real-event absolute exchange:'+tag,result['event_energy_null'],1e-10)
            records[tag]=dict(old_pair=old_pair.tolist(),new_pair=new_pair.tolist(),
                improvement=(old_pair/np.maximum(new_pair,1e-300)).tolist(),
                relative_source_change=change.tolist(),seconds=time.monotonic()-started,
                new_weighted_defect=weight*float(max(abs(new[0]+new[-1]))))
            np.savez_compressed(folder/(tag+'.npz'),old=old,new=new,weight=weight,identity=json.dumps(node,sort_keys=True))
            inputs.append(prior_path)
            print(json.dumps(dict(case=tag,record=records[tag])),flush=True)
    finish(folder,dict(checks=checks,records=records,probes=8,full_correlated_source_computed=False,
        gas_equals_minus_photon_enforced=False),__file__,inputs)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
