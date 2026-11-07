from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import json
import math
import re
import time
import numpy as np
from scipy import integrate,interpolate,linalg,special

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'coupled-finite-wave-evolution-20261007'
sys.path.insert(0,str(PARENT))
import evolution_common as inherited
modest=inherited.modest
digest=inherited.digest
NATIVE=inherited.NATIVE
COLLISION=inherited.COLLISION
HISTORY=inherited.HISTORY
I3_PLANCK=np.pi**4/15


def write_json(path,value):
    def convert(item):
        if isinstance(item,np.generic):
            return item.item()
        if isinstance(item,np.ndarray):
            return item.tolist()
        raise TypeError(type(item).__name__)
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False,default=convert),encoding='utf-8')


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'thermal_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def planck(frequency):
    return 1/np.expm1(frequency)


def weight(frequency):
    occupation=planck(frequency)
    return occupation*(1+occupation)


class ThermalBackground:
    def __init__(self,label):
        self.parent=inherited.Background(label)
        self.label=label
        self.start_scale=1e-6
        self.end_scale=1e-5
        self.native_constants=NATIVE/'fortran/constants.f90'
        text=self.native_constants.read_text()
        def constant(name):
            match=re.search(r'\b'+re.escape(name)+r'\s*=\s*([0-9.eE+-]+)_dl',text,re.I)
            assert match,name
            return float(match.group(1))
        self.constants={name:constant(name) for name in ['k_B','m_e','c','G','sigma_thomson','Mpc','m_H','m_He4']}
        self.temperature0=float(self.parent.native.Params.TCMB)
        self.theta0=self.constants['k_B']*self.temperature0/(self.constants['m_e']*self.constants['c']**2)
        helium=float(self.parent.native.Params.YHe)
        self.helium_fraction=helium
        helium_number=helium/(1-helium)*self.constants['m_H']/self.constants['m_He4']
        self.particles_per_electron=(2+3*helium_number)/(1+2*helium_number)
        electron0=self.parent.opacity_constant/(self.constants['sigma_thomson']*self.constants['Mpc'])
        photon_energy0=self.parent.photons*self.constants['c']**4/(8*np.pi*self.constants['G']*self.constants['Mpc']**2)
        self.chi=1.5*self.particles_per_electron*electron0*self.constants['k_B']*self.temperature0/photon_energy0
        self.electron0=electron0
        self.photon_energy0=photon_energy0
        self.end=math.log(self.end_scale/self.start_scale)

    def at(self,log_expansion):
        scale=self.start_scale*math.exp(log_expansion)
        moment=self.parent.time_at(scale)
        background=self.parent.at(moment)
        coefficient=background['opacity']*self.theta0/scale/background['hubble']
        return dict(scale=scale,moment=moment,hubble=background['hubble'],coefficient=coefficient,
            thermal_parameter=self.theta0/scale,relaxation_over_hubble=4*coefficient/self.chi)


class SpectralGrid:
    def __init__(self,count=800,minimum=1e-4,maximum=40.):
        self.count=count
        self.edges=np.geomspace(minimum,maximum,count+1)
        nodes,weights=np.polynomial.legendre.leggauss(8)
        widths=np.diff(self.edges)
        points=(self.edges[:-1,None]+self.edges[1:,None])/2+widths[:,None]*nodes/2
        quadrature=widths[:,None]*weights/2
        self.mass=np.sum(quadrature*points**2*weight(points),axis=1)
        energy_mass=np.sum(quadrature*points**3*weight(points),axis=1)
        self.frequency=energy_mass/self.mass
        self.energy=energy_mass/I3_PLANCK
        distance=np.diff(self.frequency)
        self.conductivity=self.edges[1:-1]**4*weight(self.edges[1:-1])
        rate=self.conductivity/distance
        self.lower=rate/self.mass[1:]
        self.upper=rate/self.mass[:-1]
        self.diagonal=np.zeros(count)
        self.diagonal[:-1]-=self.upper
        self.diagonal[1:]-=self.lower
        flux=np.r_[0.,-self.conductivity,0.]
        self.temperature_source=np.diff(flux)/self.mass
        self.temperature_energy=float(self.energy@self.temperature_source)

    def apply(self,potential):
        output=self.diagonal*potential
        output[:-1]+=self.upper*potential[1:]
        output[1:]+=self.lower*potential[:-1]
        return output

    def solve(self,alpha,coefficient,rhs):
        banded=np.zeros((3,self.count))
        banded[0,1:]=-coefficient*self.upper
        banded[1]=alpha-coefficient*self.diagonal
        banded[2,:-1]=-coefficient*self.lower
        return linalg.solve_banded((1,1),banded,rhs,check_finite=False)

    def source(self,potential,temperature):
        flux=np.r_[0.,self.conductivity*(np.diff(potential)/np.diff(self.frequency)-temperature),0.]
        return np.diff(flux)/self.mass
