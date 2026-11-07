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
import numpy as np
from scipy import integrate, interpolate

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'adiabatic-curvature-seed-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
TABLES=BRANCH/'native-two-field-transfer-20261007/runs/backgrounds'
sys.path.insert(0,str(BRANCH/'resolved-matter-spectrum-20261007'))
import spectrum_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
camb=inherited.camb
FINAL=math.log(.000265)


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'onset_common.py',ROOT/'ACCEPTANCE.md',
        PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def native_for(label):
    source=TABLES/('heavy.npz' if label=='heavy' else 'cold.npz')
    params=inherited.inherited.params_for(source)
    if label=='lcdm':
        params.DarkEnergy=camb.dark_energy.DarkEnergyFluid()
    native=camb.get_background(params)
    native.Params.Accuracy.IntTolBoost=6
    return source,native


class Background:
    def __init__(self,label,grid):
        self.label=label
        self.source=TABLES/('heavy.npz' if label=='heavy' else 'cold.npz')
        self.table=np.load(self.source)
        self.grid=grid
        self.nodes=grid['efold']
        self.nu_log=interpolate.CubicSpline(self.nodes,np.log(grid['nu']))
        self.constants={key:float(grid[key][0]) for key in ['cdm','baryon','photon','neutrino']}
        self.vacuum=float(grid['de'][-1]/np.exp(4*self.nodes[-1])) if label=='lcdm' else 0.
        self.suffixes=[] if label=='lcdm' else (['s','h'] if label=='heavy' else ['s'])
        self.masses=np.array([float(self.table['slow_mass_mpc' if suffix=='s' else 'heavy_mass_mpc']) for suffix in self.suffixes])
        self.amplitudes=np.array([float(self.table['phi_'+suffix][0]) for suffix in self.suffixes])
        self.fields=len(self.suffixes)

    def fluids(self,efold):
        scale=math.exp(efold)
        dust=(self.constants['cdm']+self.constants['baryon'])/scale**3
        dust/=math.exp(self.nodes[0])
        photon=self.constants['photon']/scale**4
        massless=self.constants['neutrino']/scale**4
        derivatives=[float(self.nu_log(efold,order)) for order in range(3)]
        massive=math.exp(derivatives[0]-4*efold)
        pressure=massive*(1-derivatives[1])/3
        pressure_n=massive*((derivatives[1]-4)*(1-derivatives[1])-derivatives[2])/3
        density=dust+photon+massless+massive+self.vacuum
        enthalpy=dust+4*(photon+massless)/3+massive+pressure
        pressure_response=4*(photon+massless)/9-pressure_n/3
        shear=np.array([4*massless/15,-pressure_n/5])
        neutrino_pressure_response=np.array([4*massless/9,-pressure_n/3])
        return density,enthalpy,pressure_response,photon,shear,neutrino_pressure_response

    def unpack(self,efold,state):
        fields=state[:4*self.fields].reshape(self.fields,4)
        ratio,velocity,field_response,derivative_response=fields.T if self.fields else (np.array([]),)*4
        volume,shear,shear_rate,current_pg,current_massless,current_massive=state[4*self.fields:]
        density,enthalpy,pressure_response,photon,nu_shear,nu_pressure=self.fluids(efold)
        field=self.amplitudes*ratio
        field_dot=self.amplitudes*self.masses*velocity
        hubble2=(density+np.sum((field_dot**2+(self.masses*field)**2)/2))/3
        hubble=math.sqrt(hubble2)
        omega=self.masses/hubble
        field_n=field_dot/hubble
        logarithmic_hubble=-(enthalpy+np.sum(field_dot**2))/(2*hubble2)
        energy=-enthalpy/hubble2*volume+np.sum(field_n*self.amplitudes*derivative_response+omega**2*field*self.amplitudes*field_response)
        pressure=-pressure_response/hubble2*volume+np.sum(field_n*self.amplitudes*derivative_response-omega**2*field*self.amplitudes*field_response)
        volume_rate=(2*energy-1)/4
        momentum=2*volume_rate/3-shear_rate/12-current_pg-current_massless-current_massive+np.sum(field_n*self.amplitudes*field_response)
        return dict(fields=fields,H=hubble,omega=omega,phi=field,phi_dot=field_dot,phi_n=field_n,h=logarithmic_hubble,
            energy=energy,pressure=pressure,volume_rate=volume_rate,momentum=momentum,enthalpy=enthalpy,
            photon=photon,nu_shear=nu_shear,nu_pressure=nu_pressure)

    def rhs(self,efold,state):
        data=self.unpack(efold,state)
        output=np.empty_like(state)
        stretch=2*(1+data['h'])
        for index,(ratio,velocity,response,response_n) in enumerate(data['fields']):
            omega=data['omega'][index]
            output[4*index:4*index+4]=[
                omega*velocity,-3*velocity-omega*ratio,
                response_n+stretch*response,
                (data['h']-1)*response_n-omega**2*response-data['volume_rate']*omega*velocity]
        volume,shear,shear_rate,current_pg,current_massless,current_massive=state[4*self.fields:]
        output[4*self.fields:]=[
            data['volume_rate']+stretch*volume,
            shear_rate+stretch*shear,
            (data['h']-1)*shear_rate-2*np.sum(data['nu_shear'])/data['H']**2*shear-2,
            (data['h']-1)*current_pg+4*data['photon']/(9*data['H']**2)*volume,
            *[(data['h']-1)*current+(pressure*volume+stress*shear/6)/data['H']**2
                for current,pressure,stress in zip([current_massless,current_massive],data['nu_pressure'],data['nu_shear'])]]
        return output

    def initial(self,start):
        state=np.zeros(4*self.fields+6)
        for index,suffix in enumerate(self.suffixes):
            nodes=self.table['efold' if suffix=='s' else 'heavy_efold']
            field=float(interpolate.CubicSpline(nodes,self.table['phi_'+suffix])(start))
            conformal=float(interpolate.CubicSpline(nodes,self.table['phidot_'+suffix])(start))
            state[4*index]=field/self.amplitudes[index]
            state[4*index+1]=conformal/(math.exp(start)*self.masses[index]*self.amplitudes[index])
        data=self.unpack(start,state)
        photon=self.constants['photon']
        massless=self.constants['neutrino']
        massive=math.exp(float(self.nu_log(start)))
        fractions=np.array([massless,massive])/(photon+massless+massive)
        denominator=1+4*sum(fractions)/15
        for index,omega in enumerate(data['omega']):
            state[4*index+2]=-omega**2/1680
            state[4*index+3]=-omega**2/280
        state[4*self.fields:]=[-1/16,-1/(3*denominator),-2/(3*denominator),
            -(1-sum(fractions))/36,*(-fractions/36*(1+8/(15*denominator)))]
        return state

    def solve(self,start,rtol):
        atol=np.full(4*self.fields+6,rtol*1e-3)
        for index,suffix in enumerate(self.suffixes):
            atol[4*index+1]=1e-28 if suffix=='s' else 1e-18
            atol[4*index+2:4*index+4]=1e-45 if suffix=='s' else 1e-25
        result=integrate.solve_ivp(self.rhs,(start,FINAL),self.initial(start),method='DOP853',
            rtol=rtol,atol=atol,max_step=.025,dense_output=True)
        assert result.success,result.message
        return result


def physical(model,efolds,states):
    records=[]
    for efold,state in zip(efolds,states.T):
        data=model.unpack(float(efold),state)
        scale=math.exp(efold)
        conformal2=(scale*data['H'])**2
        volume,shear,shear_rate=state[4*model.fields:4*model.fields+3]
        record=[data['H'],volume/conformal2,shear/conformal2,data['volume_rate']/(scale**2*data['H']),data['momentum'],data['energy']/scale**2,data['pressure']/scale**2]
        for index in range(model.fields):
            response=model.amplitudes[index]*data['fields'][index,2]/conformal2
            response_dot=model.amplitudes[index]*data['fields'][index,3]/(scale**2*data['H'])
            record.extend([data['phi'][index],data['phi_dot'][index],response,response_dot])
        records.append(record)
    names=['H','s','b','sdot','momentum_scaled','Ehat','Phat']
    for suffix in model.suffixes:
        names.extend(['phi_'+suffix,'dotphi_'+suffix,'f_'+suffix,'dotf_'+suffix])
    return names,np.array(records).T
