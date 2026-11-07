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
PARENT=BRANCH/'conserved-source-transport-20261007'
sys.path.insert(0,str(PARENT))
import transport_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
SPECTRUM=inherited.SPECTRUM
NATIVE=inherited.NATIVE
INITIAL=math.log(.5)
FINAL=-math.log(1.38)


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'feedback_common.py',ROOT/'ACCEPTANCE.md',
        PARENT/'results/stage-integrity.json',PARENT/'transport_common.py',
        SPECTRUM/'spectrum_common.py',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


class NativeSeed:
    def __init__(self,label,wave,method='cubic'):
        self.label=label
        self.wave=wave
        packet,fields=inherited.fields(label)
        self.packet=packet
        self.mode=int(np.argmin(abs(packet['modes']-wave)))
        assert abs(packet['modes'][self.mode]-wave)<1e-12
        values=packet['values'][self.mode]
        names=packet['names']
        scale=values[:,names.index('a')]
        hubble=values[:,names.index('H')]
        coordinate=np.log(scale)
        chosen=scale>.08
        factory=interpolate.CubicSpline if method=='cubic' else interpolate.PchipInterpolator
        self.log_hubble=factory(coordinate[chosen],np.log(hubble[chosen]))
        self.scale=scale
        self.hubble=hubble
        background=np.load(SPECTRUM/'runs'/label/'background.npz')
        self.source_constants=[float(np.median(background[name]/packet['scales'])) for name in ['cdm','baryon']]
        self.species=['cdm','baryon']
        shear=fields['shear'][self.mode]
        shift=3*hubble*shear/wave
        density=[values[:,names.index('delta_cdm')]-shift,values[:,names.index('delta_baryon')]-shift]
        velocity=[values[:,names.index('v_newtonian_cdm')],values[:,names.index('v_newtonian_baryon')]]
        self.mass=None
        self.paths=[SPECTRUM/'runs'/label/'background.npz',*sorted((SPECTRUM/'runs'/label).glob('chunk-*.npz'))]
        if label=='heavy':
            status=json.loads((SPECTRUM/'runs/heavy/status.json').read_text())
            path=SPECTRUM/'runs/projection'/(status['arguments']['projection']+'.npz')
            table=np.load(path)
            constant=float(table['matching_density'])
            self.source_constants.append(constant)
            self.mass=float(table['heavy_mass_mpc'])
            rho=constant/scale
            density.append(values[:,names.index('mts_drho_h')]/rho-shift)
            velocity.append(-wave*(values[:,names.index('mts_q_h')]/rho+shear)/hubble)
            self.species.append('heavy')
            self.paths.append(path)
        self.source_constants=np.array(self.source_constants)
        self.density=np.array(density)
        self.velocity=np.array(velocity)
        self.initial=int(np.argmin(abs(coordinate-INITIAL)))
        self.final=int(np.argmin(abs(coordinate-FINAL)))
        assert abs(coordinate[self.initial]-INITIAL)<1e-8
        assert abs(coordinate[self.final]-FINAL)<1e-8

    def coefficients(self,coordinate):
        scale=np.exp(coordinate)
        hubble=np.exp(self.log_hubble(coordinate))
        friction=1+self.log_hubble(coordinate,1)
        gravity=self.source_constants/(2*scale*hubble**2)
        pressure=np.zeros(len(gravity))
        if self.mass:
            pressure[-1]=self.wave**4/(4*self.mass**2*scale**2*hubble**2)
        return float(friction),gravity,pressure

    def seed(self,normalization):
        size=len(self.species)
        state=np.zeros((4,size))
        state[0]=self.density[:,self.initial]/normalization
        state[1]=self.velocity[:,self.initial]/normalization
        return state.ravel()


def harmonic_rhs(coordinate,state,coefficients,feedback=True,quadratic_pressure=True):
    density,velocity,second_density,second_velocity=np.reshape(state,(4,-1))
    friction,gravity,pressure=coefficients(coordinate)
    first_force=np.dot(gravity,density)
    second_force=np.dot(gravity,second_density)
    result=np.empty((4,len(density)))
    result[0]=velocity
    result[1]=-friction*velocity+first_force-pressure*density
    result[2]=second_velocity+density*velocity
    result[3]=-friction*second_velocity+second_force-16*pressure*second_density+velocity**2
    if quadratic_pressure:
        result[3]+=3*pressure*density**2
    if not feedback:
        result[3]=0.
    return result.ravel()


def solve_harmonics(initial,coefficients,start=INITIAL,end=FINAL,tight=True,feedback=True,quadratic_pressure=True):
    result=integrate.solve_ivp(lambda coordinate,state:harmonic_rhs(coordinate,state,coefficients,feedback,quadratic_pressure),
        (start,end),initial,method='DOP853',rtol=2e-11 if tight else 2e-8,
        atol=2e-13 if tight else 2e-10,max_step=.006 if tight else .025,dense_output=True)
    assert result.success and np.isfinite(result.y).all()
    return result


def solve_periodic(initial,coefficients,amplitude,count,start=INITIAL,end=FINAL):
    density,velocity,_,_=np.reshape(initial,(4,-1))
    size=len(density)
    phase=2*math.pi*np.arange(count)/count
    frequencies=np.fft.fftfreq(count,d=1/count)
    frequencies[count//2]=0
    initial_grid=np.concatenate([1+amplitude*density[:,None]*np.cos(phase),
        -amplitude*velocity[:,None]*np.sin(phase)]).ravel()
    min_seen=1.
    def derivative(array,order=1):
        return np.fft.ifft(np.fft.fft(array,axis=-1)*(1j*frequencies)**order,axis=-1).real
    def equation(coordinate,state):
        nonlocal min_seen
        number,flow=state.reshape(2,size,count)
        min_seen=min(min_seen,float(number.min()))
        assert number.min()>0
        friction,gravity,pressure=coefficients(coordinate)
        source=np.sum(gravity[:,None]*(number-1),axis=0)
        source_modes=np.fft.fft(source)
        potential_modes=np.zeros_like(source_modes)
        mask=frequencies!=0
        potential_modes[mask]=-source_modes[mask]/frequencies[mask]**2
        force=-np.fft.ifft(1j*frequencies*potential_modes).real
        root=np.sqrt(number)
        quantum=2*pressure[:,None]*derivative(derivative(root,2)/root)
        return np.concatenate([-derivative(number*flow),-friction*flow-flow*derivative(flow)+force+quantum]).ravel()
    result=integrate.solve_ivp(equation,(start,end),initial_grid,method='DOP853',
        rtol=2e-10,atol=2e-12,max_step=.002)
    assert result.success
    number,flow=result.y[:,-1].reshape(2,size,count)
    second_density=2*np.mean((number-1)*np.cos(2*phase),axis=1)/amplitude**2
    second_velocity=-4*np.mean(flow*np.sin(2*phase),axis=1)/amplitude**2
    return dict(second_density=second_density.tolist(),second_velocity=second_velocity.tolist(),
        min_density_seen=min_seen,max_mass_error=float(np.max(abs(number.mean(axis=1)-1))),
        nfev=result.nfev,amplitude=amplitude,count=count)
