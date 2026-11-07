from stage162_common import *


class StableJumpProbe(FastSplit):
    def born_jumps(self,parameters):
        self.jump_parameters=parameters
        self.jump_soft=None
        self.jump_direction=None
        return super().born_jumps(parameters)

    def event_products(self,parameters,soft,direction,chemical=False):
        self.jump_parameters=parameters
        self.jump_soft=soft
        self.jump_direction=direction
        return super().event_products(parameters,soft,direction,chemical)

    def jumps(self,incoming,hard,soft,electron):
        left,right=super().jumps(incoming,hard,soft,electron)
        parameters=self.jump_parameters
        energy=parameters['energy']
        angular=1-parameters['cosine']
        if self.jump_soft is None:
            delta_energy=-energy**2*angular/(1+energy*angular)
            recoil=np.array([0.,0.,energy])-parameters['hard']*parameters['hard_direction']
            number=0.
        else:
            signed_soft=self.jump_soft
            direction=self.jump_direction
            mixed=1-parameters['hard_direction']@direction
            incident_soft=1-direction[2]
            denominator=1+energy*angular-signed_soft*mixed
            outgoing=(energy-signed_soft-energy*signed_soft*incident_soft)/denominator
            delta_energy=(-energy*signed_soft*incident_soft-(energy-signed_soft)*(energy*angular-signed_soft*mixed))/denominator
            recoil=np.array([0.,0.,energy])-outgoing[:,None]*parameters['hard_direction']-signed_soft[:,None]*direction
            number=np.sign(signed_soft)
        photon=(parameters['transform'][0,0]*delta_energy-recoil@parameters['transform'][0,1:])/parameters['temperature']
        left[...,0]=photon
        left[...,1]=number/self.spectra.basis.norms[0]
        left[...,2]=(photon-self.spectra.basis.mean*number)/self.spectra.basis.norms[1]
        return left,right


def main():
    modest()
    folder=ROOT/'results/stable-jump-probe'
    folder.mkdir(parents=True,exist_ok=False)
    diagnosis=json.loads((ROOT/'PRECISION-DIAGNOSIS.json').read_text())
    proof=verify_packet(ROOT/'results/preflight')
    checks,records,inputs=[],{},[ROOT/'PRECISION-DIAGNOSIS.json',ROOT/'results/preflight/status.json',ROOT/'STABLE-JUMP-DERIVATION.md']
    for endpoint in ENDPOINTS:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        model=StableJumpProbe(bundle,'difference')
        theta=proof['contexts'][endpoint][0]['theta']
        inputs.extend(bundle.inputs)
        for case in diagnosis['top_events'][endpoint+'-65'][:2]:
            order,index=case['order'],case['index']
            node=list(integration_nodes(theta,order))[index]
            old,weight,path,loop_path=load_node162(endpoint,order,node,theta)
            parameters,unused=parameters_and_weight(theta,node)
            result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
            new=result['total']
            old_values=old['difference']
            basis=bundle.basis
            old_pair=abs(old_values[0]+old_values[-1])/np.maximum(abs(old_values[0]),1e-300)
            new_pair=abs(new[0]+new[-1])/np.maximum(abs(new[0]),1e-300)
            new_moment=abs(basis.temperature@new[1:-1]-new[0])/np.maximum(abs(new[0]),1e-300)
            tag=endpoint+f'-order{order}-node{index}'
            norm=SourceNorm(basis.mass)
            spectral_change=norm(new-old_values)/np.maximum(norm(old_values),1e-300)
            assert np.array_equal(new[3:],old_values[3:])
            test(checks,'Stable independent photon/gas:'+tag,float(max(new_pair)),1e-10)
            test(checks,'Stable analytic test-function moments:'+tag,float(max(new_moment)),1e-10)
            test(checks,'Retained spectral physical result:'+tag,float(max(spectral_change)),1e-10)
            records[tag]=dict(old_pair_relative=old_pair.tolist(),new_pair_relative=new_pair.tolist(),
                new_moment_relative=new_moment.tolist(),spectral_change=spectral_change.tolist(),
                improvement_factor=(old_pair/np.maximum(new_pair,1e-300)).tolist(),source_path=str(path),
                independent_electron_moment_preserved=True,source_adopted=False)
            np.savez_compressed(folder/(tag+'.npz'),old=old_values,new=new,mass=basis.mass,temperature=basis.temperature,
                weight=weight,identity=json.dumps(node,sort_keys=True))
            inputs.extend([path,loop_path])
            print(json.dumps(dict(case=tag,record=records[tag])),flush=True)
    finish(folder,dict(checks=checks,records=records,probe_events=4,
        full_source_recomputed=False,temperature_curve_changed=False,gas_equals_minus_photon_enforced=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks))),flush=True)


if __name__=='__main__':
    main()
