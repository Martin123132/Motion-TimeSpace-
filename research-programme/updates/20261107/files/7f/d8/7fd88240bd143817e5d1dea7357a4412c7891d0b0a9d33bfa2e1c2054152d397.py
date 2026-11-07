from stage163_common import *
from probe_stable_jumps import StableJumpProbe


class PrimitiveTests:
    def evaluate(self,frequency):
        values=np.asarray(frequency)
        if np.any(values<1e-6*(1-1e-10)) or np.any(values>60*(1+1e-10)):
            raise ValueError('Primitive test evaluation outside explicit spectral domain')
        return np.stack([values,np.ones_like(values)],axis=-1)

    def derivative(self,frequency):
        values=np.asarray(frequency)
        return np.stack([np.ones_like(values),np.zeros_like(values)],axis=-1)


class StableMoments(FastSplit):
    def __init__(self,spectra):
        self.spectra=spectra
        self.tests=PrimitiveTests()
        self.gas=np.repeat(spectra.gas,2)
        self.mode='difference'
        self.grams={}
        self.angular_cache={}

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
        left[...,0]=(parameters['transform'][0,0]*delta_energy-recoil@parameters['transform'][0,1:])/parameters['temperature']
        left[...,1]=number
        return left,right


def components(parameters,model,scalar):
    result=model.real(parameters,angular=4,radial=18,rule=PanelRule(.5))
    weak.vacuum.mp.mp.dps=60
    vacuum=float(weak.vacuum.finite_virtual_ratio(parameters['energy'],parameters['cosine'])
        +weak.vacuum.soft_constant(parameters['energy'],parameters['cosine']))
    jump,product=model.born_data(parameters)
    return dict(difference=result['total'],virtual=.5*(vacuum+scalar)*product,
        state=model.state_correction(parameters)['total']),result['event_energy_null']
