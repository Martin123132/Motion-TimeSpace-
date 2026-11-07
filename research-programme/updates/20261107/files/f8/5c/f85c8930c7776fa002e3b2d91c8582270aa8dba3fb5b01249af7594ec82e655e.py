from stage164_common import *
from stable_moments import StableMoments
from reconcile_reference import cardinal_weights
import mpmath as mp


def exact_born_left(parameters):
    energy=mp.mpf(float(parameters['energy']))
    cosine=mp.mpf(float(parameters['cosine']))
    temperature=mp.mpf(float(parameters['temperature']))
    direction=[mp.sqrt(1-cosine*cosine),mp.mpf(0),cosine]
    hard=energy/(1+energy*(1-cosine))
    recoil=[-hard*direction[0],mp.mpf(0),energy-hard*direction[2]]
    kinetic=sum(value*value for value in recoil)
    kinetic/=mp.sqrt(1+kinetic)+1
    photon_rest=-energy*energy*(1-cosine)/(1+energy*(1-cosine))
    temporal=[mp.mpf(float(value)) for value in parameters['transform'][0]]
    boost=sum(temporal[index+1]*recoil[index] for index in range(3))
    return [((temporal[0]*photon_rest-boost)/temperature),mp.mpf(0),((temporal[0]*kinetic+boost)/temperature)]


def outer(left,right):
    return mp.matrix([[value*mp.mpf(float(other)) for other in right] for value in left])


class PreciseBornCorrelated(CorrelatedSoft):
    def born_jumps(self,parameters):
        left,right=super().born_jumps(parameters)
        with mp.workdps(80):
            left=np.array([float(value) for value in exact_born_left(parameters)])
        return left,right


def precise_state(parameters,model,digits):
    with mp.workdps(digits):
        old_left,right=model.born_jumps(parameters)
        left=exact_born_left(parameters)
        product=outer(left,right)
        response=weak.source.previous.phase_response(mp.mpf(str(parameters['energy'])),
            mp.mpf(str(parameters['cosine'])),mp.mpf(str(parameters['temperature'])))
        temporal=[mp.mpf(float(value)) for value in parameters['transform'][0]]
        temperature=mp.mpf(float(parameters['temperature']))
        photon_delta=sum(temporal[index]*response['photon_delta'][index] for index in range(4))/temperature
        electron_delta=sum(temporal[index]*response['electron_delta'][index] for index in range(4))/temperature
        outgoing=parameters['hard']*parameters['hard_doppler']/parameters['temperature']
        derivatives=model.spectra.derivatives(outgoing)[1:]
        right_shift=[mp.mpf(float(derivatives[index]))*photon_delta+mp.mpf(float(model.gas[index]))*electron_delta for index in range(4)]
        observable=outer([photon_delta,mp.mpf(0),electron_delta],right)
        observable+=mp.matrix([[value*other for other in right_shift] for value in left])
        observable/=2
        bose_delta=-mp.mpf(float(parameters['hard_bose']-1))*photon_delta
        phase=(response['phase_delta']+bose_delta)*product/2
        velocity=parameters['velocity']
        gamma_squared=1/(1-velocity@velocity)
        tangent=-velocity/(2*gamma_squared)
        step=1e-3
        samples=[]
        for offset in [2*step,step,-step,-2*step]:
            shifted=weak.source.context(parameters['lab_energy'],parameters['lab_cosine'],velocity+offset*tangent,parameters['temperature'])
            unused,shifted_right=model.born_jumps(shifted)
            samples.append(mp.mpf(float(shifted['born_differential_over_thomson']))*outer(exact_born_left(shifted),shifted_right)/2)
        canonical=response['mass_squared']*(-samples[0]+8*samples[1]-8*samples[2]+samples[3])/mp.mpf(12*step)
        canonical/=mp.mpf(float(parameters['born_differential_over_thomson']))
        score=weak.normalized_mass_score(gamma_squared*(velocity@velocity),parameters['temperature'])
        population=response['mass_squared']*mp.mpf(float(score))*product/2
        parts=dict(phase=phase,observable_shift=observable,canonical=canonical,population=population)
        parts['total']=phase+observable+canonical+population
        relative={name:max(float(abs(values[0,column]+values[2,column])/max(abs(values[0,column]),mp.mpf('1e-300'))) for column in range(4)) for name,values in parts.items()}
        arrays={name:np.array(values.tolist(),dtype=float) for name,values in parts.items()}
        return arrays,relative


def main():
    modest()
    folder=ROOT/'results/state-roundoff-probe'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    diagnosis=verify_packet(ROOT/'results/phase-diagnosis')
    checks,records,inputs=[],{},[ROOT/'results/preflight/status.json',ROOT/'results/phase-diagnosis/status.json',ROOT/'STATE-ROUNDOFF-DERIVATION.md']
    phase=diagnosis['records']['terminal-cubic-65']['pair']['phase']
    weights=cardinal_weights(phase,'cubic')
    for endpoint,weight_index in [('start',0),('end',4)]:
        bundle=EpochBundle(ENDPOINTS[endpoint])
        model=StableMoments(bundle)
        born_model=PreciseBornCorrelated(bundle)
        inputs.extend(bundle.inputs)
        theta=proof['contexts'][endpoint][0]['theta']
        for order in [4,5,6]:
            ranked=[]
            for node in integration_nodes(theta,order):
                path=moment_path(endpoint,order,node['index'])
                saved=read_npz(path)
                maximum=abs(weights[weight_index]*float(saved['weight']))*float(max(abs(saved['state'][0]+saved['state'][-1])))
                ranked.append((maximum,node,path))
            ranked.sort(key=lambda item:item[0],reverse=True)
            for maximum,node,path in ranked[:2]:
                parameters,weight=parameters_and_weight(theta,node)
                saved=read_npz(path)
                with mp.workdps(60):
                    old=model.state_correction(parameters)
                high,identities=precise_state(parameters,model,80)
                low,unused=precise_state(parameters,model,50)
                tag=f'{endpoint}-order{order}-node{node["index"]}'
                old_rounding={name:float(max(abs(values[0]+values[-1])/np.maximum(abs(values[0]),1e-300))) for name,values in old.items()}
                test(checks,'Independent high-precision state energy:'+tag,max(identities.values()),1e-10)
                close(checks,'Unchanged saved state reproduced:'+tag,old['total'],saved['state'],1e-10)
                close(checks,'50/80digit state agreement:'+tag,low['total'],high['total'],1e-10)
                close(checks,'Equivalent repaired state source:'+tag,high['total'],saved['state'],1e-10)
                result=born_model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
                real=result['total']
                old_real=saved['difference']
                close(checks,'Equivalent high-precision Born real source:'+tag,real,old_real,1e-10)
                record=dict(weighted_state_defect=maximum,old_components_pair_relative=old_rounding,
                    repaired_components_pair_relative=identities,
                    state_change=float(np.max(abs(high['total']-saved['state']))/max(np.max(abs(saved['state'])),1e-300)),
                    old_real_pair=(abs(old_real[0]+old_real[-1])/np.maximum(abs(old_real[0]),1e-300)).tolist(),
                    repaired_born_real_pair=(abs(real[0]+real[-1])/np.maximum(abs(real[0]),1e-300)).tolist(),
                    full_bank_state_repaired=False,source_adopted=False,finite_difference_step=1e-3)
                records[tag]=record
                np.savez_compressed(folder/(tag+'.npz'),old=saved['state'],new=high['total'],old_real=old_real,new_real=real,
                    identity=json.dumps(node,sort_keys=True),weight=weight,**{name:values for name,values in high.items() if name!='total'})
                inputs.append(path)
                print(json.dumps(dict(case=tag,record=record)),flush=True)
    finish(folder,dict(checks=checks,records=records,probes=len(records),state_full_bank_repaired=False,
        source_adopted=False,temperature_curve_changed=False,gas_equals_minus_photon_assigned=False),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
