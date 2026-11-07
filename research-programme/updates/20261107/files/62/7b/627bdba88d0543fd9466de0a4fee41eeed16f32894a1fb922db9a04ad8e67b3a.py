from common import *
import numpy as np
from numpy.polynomial.legendre import leggauss


FERMI=7*np.pi**4/120
PANELS=(0.,.1,1.,3.,10.,30.,90.)


def parameters(native):
    count=native.Params.nu_mass_eigenstates
    return dict(cdm=float(native.grhoc),baryon=float(native.grhob),photon=float(native.grhog),
                massless=float(native.grhornomass),masses=list(native.nu_masses)[:count],
                coefficients=list(native.grhormass)[:count],curvature=float(native.grhok))


class Thermal:
    def __init__(self,parameters,order=48):
        self.parameters=parameters
        self.order=order
        nodes,weights=leggauss(order)
        self.nodes=np.concatenate([left+(right-left)*(nodes+1)/2 for left,right in zip(PANELS[:-1],PANELS[1:])])
        self.weights=np.concatenate([(right-left)*weights/2 for left,right in zip(PANELS[:-1],PANELS[1:])])
        self.weights*=np.exp(-self.nodes)/(1+np.exp(-self.nodes))*self.nodes**2/FERMI
        require(np.all(self.weights>0),'positive thermal quadrature')
        require(parameters['curvature']==0,'retained flat source')

    def values(self,efold):
        efold=np.atleast_1d(efold).astype(float)
        output=np.empty((len(efold),3))
        for first in range(0,len(efold),256):
            guard()
            scale=np.exp(efold[first:first+256])
            cold=(self.parameters['cdm']+self.parameters['baryon'])/scale
            radiation=(self.parameters['photon']+self.parameters['massless'])/scale**2
            result=np.stack([cold+radiation,-cold-2*radiation,cold+4*radiation],axis=1)
            for mass,coefficient in zip(self.parameters['masses'],self.parameters['coefficients']):
                energy=np.sqrt(self.nodes[None,:]**2+(mass*scale[:,None])**2)
                speed2=(self.nodes[None,:]/energy)**2
                density=coefficient/scale[:,None]**2*energy*self.weights[None,:]
                result[:,0]+=density.sum(axis=1)
                result[:,1]+=(-density*(1+speed2)).sum(axis=1)
                result[:,2]+=(density*(1+4*speed2-speed2**2)).sum(axis=1)
            output[first:first+256]=result
        return output

    def tail_bounds(self,efold):
        scale=np.exp(np.atleast_1d(efold))
        bound=np.zeros_like(scale)
        cutoff=PANELS[-1]
        third=np.exp(-cutoff)*(cutoff**3+3*cutoff**2+6*cutoff+6)
        second=np.exp(-cutoff)*(cutoff**2+2*cutoff+2)
        for mass,coefficient in zip(self.parameters['masses'],self.parameters['coefficients']):
            bound+=coefficient/scale**2*(third+mass*scale*second)/FERMI
        return np.stack([bound,2*bound,4*bound],axis=1)
