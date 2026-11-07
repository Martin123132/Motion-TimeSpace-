from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import time
import numpy as np
from scipy import integrate,interpolate,linalg,special

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'adiabatic-boundary-and-screen-transport-20261007'
GEOMETRY=BRANCH/'einstein-constraints-and-kinetic-response-20261007'
COLLISION=BRANCH/'thomson-source-coupling-20261007'
HISTORY=BRANCH/'full-history-source-precision-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
sys.path.insert(0,str(PARENT))
import boundary_common as inherited
from derive_matter_correction import coefficients as boundary_coefficients
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
collision=inherited.inherited
geometry=collision.inherited
vertex=geometry.inherited
camb=collision.camb


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'evolution_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


class Angular:
    def __init__(self,maximum=8):
        self.maximum=maximum
        self.projectors=collision.CollisionProjectors(maximum+4,2*(maximum+4))
        self.directions=self.projectors.directions
        self.weights=self.projectors.weights
        self.screen=self.projectors.screen
        polar=np.arccos(self.directions[:,2])
        azimuthal=np.arctan2(self.directions[:,1],self.directions[:,0])
        harmonics={}
        for degree in range(maximum+1):
            for order in range(-degree,degree+1):
                harmonics[(degree,order)]=special.sph_harm_y(degree,order,polar,azimuthal)
        self.modes=list(harmonics)
        self.basis=np.stack(list(harmonics.values()),axis=1)
        self.transform=4*np.pi*self.basis.conj().T*self.weights
        gradients=[]
        for degree,order in self.modes:
            raised=math.sqrt((degree-order)*(degree+order+1))*harmonics.get((degree,order+1),np.zeros(len(polar)))
            lowered=math.sqrt((degree+order)*(degree-order+1))*harmonics.get((degree,order-1),np.zeros(len(polar)))
            angular_momentum=np.column_stack([(raised+lowered)/2,(raised-lowered)/(2j),order*harmonics[(degree,order)]])
            gradients.append(-1j*np.cross(self.directions,angular_momentum))
        self.gradients=np.stack(gradients,axis=2)

    def gradient(self,values):
        shape=values.shape
        coefficients=self.transform@values.reshape(len(self.weights),-1)
        return np.einsum('nim,ma->nia',self.gradients,coefficients).reshape((len(self.weights),3)+shape[1:])

    def moments(self,intensity):
        scalar=np.trace(intensity,axis1=1,axis2=2) if intensity.ndim==3 else intensity
        energy=self.weights@scalar
        flux=np.einsum('n,ni->i',self.weights*scalar,self.directions)
        stress=np.einsum('n,ni,nj->ij',self.weights*scalar,self.directions,self.directions)
        return energy,flux,stress


class Background:
    def __init__(self,label,start_scale=2.5e-7,end_scale=1e-5):
        self.label=label
        source_name='unmatched-base.npz' if label=='heavy' else 'cold-base.npz'
        self.source=HISTORY/'runs/sources'/source_name
        table=np.load(self.source)
        params=vertex.inherited.inherited.inherited.params_for(self.source)
        native=camb.get_background(params)
        self.native=native
        self.beta=float(native.adotrad)
        self.radiation=float(native.grhog+native.grhornomass+sum(native.grhormass))
        self.photons=float(native.grhog)
        self.neutrinos=self.radiation-self.photons
        self.baryons=float(native.grhob)
        self.cold=float(native.grhoc)
        self.fraction=self.neutrinos/self.radiation
        self.mu=(self.baryons+self.cold)/(3*self.beta)
        self.baryon_share=self.baryons/(self.baryons+self.cold)
        self.masses=np.array([float(table['slow_mass_mpc']),float(table['heavy_mass_mpc'])])
        self.frozen=np.array([float(table['phi_s'][0]),float(table['phi_h'][0]) if label=='heavy' else 0.])
        self.field_splines=[interpolate.CubicSpline(table['efold'],np.column_stack([table['phi_s'],table['phidot_s']])),
            interpolate.CubicSpline(table['heavy_efold'],np.column_stack([table['phi_h'],table['phidot_h']])) if label=='heavy' else None]
        initial_fields=np.array([spline(math.log(start_scale)) if spline else [0.,0.] for spline in self.field_splines])
        self.initial_time=float(native.conformal_time(1/start_scale-1,tol=1e-10))
        final_time=float(native.conformal_time(1/end_scale-1,tol=1e-10))*1.02
        initial=np.r_[start_scale,initial_fields[:,0],initial_fields[:,1]]
        def rhs(moment,state):
            scale=state[0]
            fields=state[1:3]
            prime=state[3:5]
            energy=(self.radiation/scale**4+(self.baryons+self.cold)/scale**3+
                np.sum(prime**2/scale**2+self.masses**2*fields**2)/2)
            hubble=scale*math.sqrt(energy/3)
            return np.r_[scale*hubble,prime,-2*hubble*prime-scale**2*self.masses**2*fields]
        solution=integrate.solve_ivp(rhs,(self.initial_time,final_time),initial,method='DOP853',rtol=3e-12,atol=1e-26,dense_output=True,max_step=.02)
        assert solution.success
        self.solution=solution
        thermal=np.load(COLLISION/'runs/backgrounds'/(label+'.npz'))
        self.opacity_constant=float(thermal['opacity'][0]*thermal['scales'][0]**2)
        self.kappa0=self.opacity_constant/self.beta**2
        self.end_scale=end_scale
        self.last_time=float(interpolate.PchipInterpolator(solution.y[0],solution.t)(end_scale))

    def at(self,moment):
        state=self.solution.sol(moment)
        scale=float(state[0])
        fields=state[1:3]
        prime=state[3:5]
        photon=self.photons/scale**4
        neutrino=self.neutrinos/scale**4
        baryon=self.baryons/scale**3
        cold=self.cold/scale**3
        energy=photon+neutrino+baryon+cold+np.sum(prime**2/scale**2+self.masses**2*fields**2)/2
        return dict(scale=scale,fields=fields,prime=prime,hubble=scale*math.sqrt(energy/3),
            photon=photon,neutrino=neutrino,baryon=baryon,cold=cold,opacity=self.opacity_constant/scale**2,
            ratio=.75*baryon/photon)

    def time_at(self,scale):
        return float(interpolate.PchipInterpolator(self.solution.y[0],self.solution.t)(scale))
