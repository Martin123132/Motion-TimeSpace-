import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from annular_flat_preassembled_flow_20260916 import band_product
from annular_canonical_energy_20260917 import CanonicalEnergy


class RelativeHamiltonian:
    def __init__(self, model):
        self.model,self.count=model,model.count
        self.energy=CanonicalEnergy(model)

    def inverse_legendre(self, canonical, clock=0.):
        if np.iscomplexobj(canonical):
            raise ValueError('Inverse qualification uses real canonical states.')
        count=self.count
        field,position=canonical[:count],canonical[count]
        momentum,source_momentum=canonical[count+1:2*count+1],canonical[-1]
        matrices=self.model.matrices(position)
        cross=band_product(matrices['transport'],field)
        solved=solve_banded((2,2),matrices['mass'],np.column_stack([momentum,cross]),check_finite=False)
        loading=source_momentum-cross @ solved[:,0]
        complement=field @ band_product(matrices['square'],field)-cross @ solved[:,1]
        mass=self.model.system.source_mass
        if complement < -1e-11*max(1.,abs(field @ band_product(matrices['square'],field))):
            raise ValueError('Kinetic Cauchy-Schwarz failed.')

        def equation(speed):
            return complement*speed+mass*speed/np.sqrt(1-speed**2)-loading

        speed=brentq(equation,-1+1e-14,1-1e-14,xtol=5e-16,rtol=1e-15)
        velocity=solved[:,0]-speed*solved[:,1]
        return np.concatenate([field,[position],velocity,[speed,clock]])

    def distance(self, actual, reference, beta=1.):
        actual_map=self.energy.lagrangian(actual)
        reference_map=self.energy.lagrangian(reference)
        difference=actual_map['canonical_state']-reference_map['canonical_state']
        value=self.model.evaluate(actual,True)['energy']-self.model.evaluate(reference,True)['energy']
        value-=reference_map['Hamiltonian_gradient'] @ difference
        value+=beta*difference[self.count]**2/2
        return value

    def reduced_value(self, canonical):
        state=self.inverse_legendre(canonical)
        field,position,speed=state[:self.count],state[self.count],state[-2]
        momentum=canonical[self.count+1:2*self.count+1]
        matrices=self.model.matrices(position)
        cross=band_product(matrices['transport'],field)
        solved=solve_banded((2,2),matrices['mass'],np.column_stack([momentum,cross]),check_finite=False)
        loading=canonical[-1]-cross @ solved[:,0]
        complement=field @ band_product(matrices['square'],field)-cross @ solved[:,1]
        factor=self.model.lifted @ field
        potential=field @ band_product(matrices['bulk'],field)/2+factor @ (matrices['gram']*factor)/2
        return momentum @ solved[:,0]/2+loading*speed-complement*speed**2/2+self.model.system.source_mass*np.sqrt(1-speed**2)+potential

    def rate(self, actual, reference, reference_derivative, beta=1.):
        base=self.energy.evaluate(reference)
        moved=self.energy.lagrangian(actual)
        difference=moved['canonical_state']-base['canonical_state']
        base_flow=self.energy.canonical_J @ base['Hamiltonian_gradient']
        canonical_residual=base_flow-base['transform'] @ reference_derivative[:-1]
        metric=base['hessian'].copy()
        metric[self.count,self.count]+=beta
        gradient_remainder=moved['Hamiltonian_gradient']-base['Hamiltonian_gradient']-base['hessian'] @ difference
        principal=float(gradient_remainder @ base_flow)
        shift=float(beta*difference[self.count]*(actual[-2]-reference[-2]))
        forcing=float(difference @ metric @ canonical_residual)
        return dict(rate=principal+shift+forcing,principal=principal,shift=shift,forcing=forcing,
            difference=difference,reference_flow=base_flow,reference_canonical=base['canonical_state'])
