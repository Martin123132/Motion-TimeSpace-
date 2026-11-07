from source201 import *
from scipy.interpolate import CubicSpline


def split(values):
    scaled=134217729.*values
    high=scaled-(scaled-values)
    return high,values-high


def stable_dot(rows,high,low):
    rows=np.asarray(rows,dtype=float)
    original_shape=rows.shape[:-1]
    flat=rows.reshape(-1,rows.shape[-1])
    first,second=split(flat)
    output=np.empty((len(flat),high.shape[1]))
    for column in range(high.shape[1]):
        active=(high[:,column]!=0)|(low[:,column]!=0)
        if not active.any():
            output[:,column]=0
            continue
        values=flat[:,active]
        coefficient=high[active,column]
        coefficient_high,coefficient_low=split(coefficient)
        product=values*coefficient
        residual=((first[:,active]*coefficient_high-product)+first[:,active]*coefficient_low
                  +second[:,active]*coefficient_high)+second[:,active]*coefficient_low
        lower=values*low[active,column]
        output[:,column]=[math.fsum([*upper,*error,*tail]) for upper,error,tail in zip(product,residual,lower)]
    return output.reshape(original_shape+(high.shape[1],))


class Features:
    def __init__(self,original):
        epoch=original.epochs[0]
        self.basis=original.basis
        self.frequency=epoch.frequency
        self.splines=[]
        basis_values=epoch.basis.evaluate(epoch.frequency)
        for lower,upper in ((1e-4,2e-4),(5e-5,1e-4)):
            phase=np.clip((epoch.frequency-lower)/(upper-lower),0,1)
            blend=phase**3*(10-15*phase+6*phase**2)
            data=np.zeros((len(epoch.frequency),98))
            data[:,:96]=basis_values*blend[:,None]
            for model_index,model in enumerate(('heavy','cold')):
                frequency,slope=epoch.tails[model]
                tail=np.interp(np.log(epoch.frequency),np.log(frequency),slope)*epoch.frequency
                data[:,96+model_index]=(1-blend)*tail
            self.splines.append(CubicSpline(np.log(epoch.frequency),data,axis=0,extrapolate=False))

    def evaluate(self,frequency,join,derivative=False):
        values=np.asarray(frequency)
        assert np.all(values>=self.frequency[0]*(1-1e-10)) and np.all(values<=self.frequency[-1]*(1+1e-10))
        coordinate=np.log(np.clip(values,self.frequency[0],self.frequency[-1]))
        result=self.splines[join](coordinate,nu=1 if derivative else 0)
        return result/values[...,None] if derivative else result


class Bundle:
    def __init__(self,features,coefficients,inputs):
        self.features=features;self.basis=features.basis;self.inputs=inputs
        self.high=np.empty((99,len(coefficients)))
        self.low=np.empty_like(self.high)
        with mp.workdps(80):
            for column,values in enumerate(coefficients):
                for index,value in enumerate(values):
                    exact=mp.mpf(value)
                    self.high[index,column]=float(exact)
                    self.low[index,column]=float(exact-mp.mpf(float(exact)))
        self.gas=self.high[-1,::2].tolist()

    def apply(self,rows,join):
        columns=np.arange(join,self.high.shape[1],2)
        return stable_dot(rows,self.high[:,columns],self.low[:,columns])

    def functions(self,frequency,chemical=False):
        assert not chemical
        values=np.asarray(frequency)
        output=np.zeros(values.shape+(self.high.shape[1]+1,))
        output[...,0]=values
        for join in range(2):
            features=self.features.evaluate(values,join)
            rows=np.concatenate([features,np.zeros(values.shape+(1,))],axis=-1)
            output[...,1+join::2]=self.apply(rows,join)
        return output

    def derivatives(self,frequency,chemical=False):
        assert not chemical
        output=np.empty(self.high.shape[1]+1);output[0]=1
        for join in range(2):
            row=np.r_[self.features.evaluate(frequency,join,True),0.]
            output[1+join::2]=self.apply(row,join)
        return output

    def forms(self,incoming,hard,soft,electron):
        forms=[]
        for join in range(2):
            row=self.features.evaluate(hard,join)-self.features.evaluate(incoming,join)
            if soft is not None:
                sign,frequency=soft
                row=row+sign[...,None]*self.features.evaluate(frequency,join)
            row=np.concatenate([row,np.asarray(electron)[...,None]],axis=-1)
            forms.append(row)
        return forms

    def contract(self,forms):
        output=np.empty(forms[0].shape[:-1]+(self.high.shape[1],))
        for join in range(2):
            output[...,join::2]=self.apply(forms[join],join)
        return output

    def shifted(self,frequency,photon,electron):
        rows=[np.r_[self.features.evaluate(frequency,join,True)*float(photon),float(electron)] for join in range(2)]
        return self.contract(rows)


class Jumps:
    def jumps(self,incoming,hard,soft,electron):
        left=self.tests.evaluate(hard)-self.tests.evaluate(incoming)
        if soft is not None:
            signed,frequency=soft
            left+=signed[...,None]*self.tests.evaluate(frequency)
        left=np.concatenate([left,np.asarray(electron)[...,None]],axis=-1)
        if left.shape[-1]==3:
            parameters=self.jump_parameters
            energy=parameters['energy'];angular=1-parameters['cosine']
            if self.jump_soft is None:
                delta_energy=-energy**2*angular/(1+energy*angular)
                recoil=np.array([0.,0.,energy])-parameters['hard']*parameters['hard_direction']
                number=0.
            else:
                signed_soft=self.jump_soft;direction=self.jump_direction
                mixed=1-parameters['hard_direction']@direction
                incident_soft=1-direction[2]
                denominator=1+energy*angular-signed_soft*mixed
                outgoing=(energy-signed_soft-energy*signed_soft*incident_soft)/denominator
                delta_energy=(-energy*signed_soft*incident_soft-(energy-signed_soft)*(energy*angular-signed_soft*mixed))/denominator
                recoil=np.array([0.,0.,energy])-outgoing[:,None]*parameters['hard_direction']-signed_soft[:,None]*direction
                number=np.sign(signed_soft)
            left[...,0]=(parameters['transform'][0,0]*delta_energy-recoil@parameters['transform'][0,1:])/parameters['temperature']
            left[...,1]=number
        forms=self.spectra.forms(incoming,hard,soft,electron)
        right=self.spectra.contract(forms)
        self.last_forms=forms;self.last_right=right
        return left,right


class Full(Jumps,source.physics.FastSplit):
    def state_correction(self,parameters,step=1e-3):
        left,right=self.born_jumps(parameters)
        product=np.outer(left,right)
        response=source.physics.weak.source.previous.phase_response(mp.mpf(str(parameters['energy'])),
            mp.mpf(str(parameters['cosine'])),mp.mpf(str(parameters['temperature'])))
        photon_shift=parameters['transform']@np.array([float(value) for value in response['photon_delta']])
        electron_shift=parameters['transform']@np.array([float(value) for value in response['electron_delta']])
        outgoing=parameters['hard']*parameters['hard_doppler']/parameters['temperature']
        photon_delta=photon_shift[0]/parameters['temperature']
        electron_delta=electron_shift[0]/parameters['temperature']
        left_shift=np.r_[self.tests.derivative(outgoing)*photon_delta,electron_delta]
        right_shift=self.spectra.shifted(outgoing,photon_delta,electron_delta)
        observable=.5*(np.outer(left_shift,right)+np.outer(left,right_shift))
        bose_delta=-(parameters['hard_bose']-1)*photon_delta
        phase=.5*(float(response['phase_delta'])+bose_delta)*product
        velocity=parameters['velocity'];gamma_squared=1/(1-velocity@velocity)
        tangent=-velocity/(2*gamma_squared);delta_mass=float(response['mass_squared'])
        samples=[self.born_weak(parameters,velocity+offset*tangent) for offset in (2*step,step,-step,-2*step)]
        canonical=delta_mass*(-samples[0]+8*samples[1]-8*samples[2]+samples[3])/(12*step)
        canonical/=parameters['born_differential_over_thomson']
        score=source.physics.weak.normalized_mass_score(gamma_squared*(velocity@velocity),parameters['temperature'])
        population=.5*delta_mass*score*product
        return dict(phase=phase,observable_shift=observable,canonical=canonical,population=population,
                    total=phase+observable+canonical+population)


class Soft(Jumps,source.PreciseSoftShifts):
    def difference_product(self,parameters,soft,direction,born_left,born_right):
        density,unused,left,delta=super().difference_product(parameters,soft,direction,born_left,born_right)
        event_forms=self.last_forms
        right=self.last_right
        self.born_jumps(parameters)
        born_forms=self.last_forms
        difference_right=self.spectra.contract([event-born for event,born in zip(event_forms,born_forms)])
        difference=np.einsum('ni,nj->nij',delta,right)+np.einsum('i,nj->nij',born_left,difference_right)
        self.last_forms=event_forms;self.last_right=right
        return density,difference,left,delta


class Moments(Jumps,source.physics.StableMoments):
    pass


def precise_state(parameters,model,digits):
    with mp.workdps(digits):
        unused,right=model.born_jumps(parameters)
        left=source.physics.exact_born_left(parameters)
        product=source.physics.outer(left,right)
        response=source.physics.weak.source.previous.phase_response(mp.mpf(str(parameters['energy'])),
            mp.mpf(str(parameters['cosine'])),mp.mpf(str(parameters['temperature'])))
        temporal=[mp.mpf(float(value)) for value in parameters['transform'][0]]
        temperature=mp.mpf(float(parameters['temperature']))
        photon_delta=sum(temporal[index]*response['photon_delta'][index] for index in range(4))/temperature
        electron_delta=sum(temporal[index]*response['electron_delta'][index] for index in range(4))/temperature
        outgoing=parameters['hard']*parameters['hard_doppler']/parameters['temperature']
        underlying=model.model if hasattr(model,'model') else model
        start=model.start if hasattr(model,'start') else 0
        shifts=underlying.spectra.shifted(outgoing,photon_delta,electron_delta)[start:start+4]
        right_shift=[mp.mpf(float(value)) for value in shifts]
        observable=source.physics.outer([photon_delta,mp.mpf(0),electron_delta],right)
        observable+=mp.matrix([[value*other for other in right_shift] for value in left])
        observable/=2
        bose_delta=-mp.mpf(float(parameters['hard_bose']-1))*photon_delta
        phase=(response['phase_delta']+bose_delta)*product/2
        velocity=parameters['velocity'];gamma_squared=1/(1-velocity@velocity)
        tangent=-velocity/(2*gamma_squared);step=1e-3;samples=[]
        for offset in (2*step,step,-step,-2*step):
            shifted=source.physics.weak.source.context(parameters['lab_energy'],parameters['lab_cosine'],velocity+offset*tangent,parameters['temperature'])
            unused,shifted_right=model.born_jumps(shifted)
            samples.append(mp.mpf(float(shifted['born_differential_over_thomson']))*source.physics.outer(source.physics.exact_born_left(shifted),shifted_right)/2)
        canonical=response['mass_squared']*(-samples[0]+8*samples[1]-8*samples[2]+samples[3])/mp.mpf(12*step)
        canonical/=mp.mpf(float(parameters['born_differential_over_thomson']))
        score=source.physics.weak.normalized_mass_score(gamma_squared*(velocity@velocity),parameters['temperature'])
        population=response['mass_squared']*mp.mpf(float(score))*product/2
        parts=dict(phase=phase,observable_shift=observable,canonical=canonical,population=population)
        parts['total']=phase+observable+canonical+population
        identities={name:max(float(abs(values[0,column]+values[2,column])/max(abs(values[0,column]),mp.mpf('1e-300'))) for column in range(4)) for name,values in parts.items()}
        return {name:np.array(value.tolist(),dtype=float) for name,value in parts.items()},identities


def models(bundle):
    full={name:Full(bundle,name) for name in ('control','difference')}
    primitive={name:Soft(bundle) for name in ('control','difference')}
    primitive['control'].mode='control'
    return full,primitive,Moments(bundle)


def coefficients(original,kind):
    groups=[]
    with mp.workdps(80):
        originals=[]
        for index,model in enumerate(('heavy','cold')):
            values=[mp.mpf(float(value)) for value in original.epochs[0].original[model]]+[mp.mpf(int(index==0)),mp.mpf(int(index==1)),mp.mpf(float(original.gas[index]))]
            originals.extend([values,values])
        if kind=='actual':groups.append(originals)
        for grid in GRIDS:
            current=[];photon=[];gas=[]
            for index,model in enumerate(('heavy','cold')):
                state=read(PARENT/f'histories/{model}/{grid}/complete.json')['current']
                values=list(map(mp.mpf,state['profile']))+[mp.mpf(int(index==0)),mp.mpf(int(index==1)),mp.mpf(state['gas'])]
                difference=[value-before for value,before in zip(values,originals[2*index])]
                current.extend([values,values])
                photon.extend([difference[:98]+[mp.mpf(0)]]*2)
                gas.extend([[mp.mpf(0)]*98+[difference[98]]]*2)
            if kind=='actual':groups.append(current)
            else:groups.extend([photon,gas])
        if kind=='prediction':groups.append([[mp.mpf(0)]*99 for unused in range(4)])
    return [values for group in groups for values in group]
