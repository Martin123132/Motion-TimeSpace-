from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PREVIOUS=BRANCH/'forced-source-gravity-bound-20261026'
sys.path.insert(0,str(PREVIOUS))
import common226 as prior
inherited,parent=prior.inherited,prior.parent
np,mp,math,json=prior.np,prior.mp,prior.math,prior.json
read,write,save,packet,digest,check=prior.read,prior.write,prior.save,prior.packet,prior.digest,prior.check
register,load=prior.register,prior.load
from scipy import interpolate,linalg
SEAL='a9cfc4a9a91698d08d60d1cc60cfd2f22471c921cf8770174a4bc43bf797f403'
FIRST=parent.FIRST_FRACTION*math.log(10)
LAST=math.log(10)

def now():
    return datetime.now(timezone.utc).isoformat()

def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PREVIOUS/'results/stage-integrity.json'
    assert digest(seal_path)==SEAL
    seal=read(seal_path)
    assert seal['qualified'] and seal['state']=='complete'
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PREVIOUS/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=SEAL
    for path,value in inputs.items():
        assert digest(path)==value,path
    for path,value in seal['bookmarks'].items():
        assert digest(path)==value,path
    for model in parent.MODELS:
        folder=BRANCH/f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400'
        register(inputs,folder/'history.npz')
        report=read(register(inputs,folder/'status.json'))
        assert report['all_checks_passed'] and report['mode']=='nonlocal-leading'
        assert report['bank']=='s960-i256' and report['steps']==6400
    for relative in ('population-matched-source-20261008/population_common.py',
        'emitting-thermal-background-20261008/sourced_emission.py',
        'infrared-source-domain-20261008/evolve_nonlocal_background.py',
        'emitting-thermal-background-20261008/evolve_emitting_background.py'):
        register(inputs,BRANCH/relative)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',dict(stage=227,turn_start='2026-10-26T16:18:33+00:00',frozen_at=now(),
        previous_goal_turn='progress',previous_seal=SEAL,models=list(parent.MODELS),working_digits=80,
        interval=[FIRST,LAST],identity_tolerance=1e-10,representation_tolerance=1e-10,refinement_tolerance=.01,
        counts=[2048,4096],coupled_probes=[parent.FIRST_FRACTION,(parent.FIRST_FRACTION+parent.LAST_FRACTION)/2,parent.LAST_FRACTION],
        reference='Original 6400-step weak-kinetic profiles with their inherited linear interpolation, not the history delta',
        bank_changed=False,curve_changed=False,grids_changed=False,tolerances_changed=False,
        protocol_hashes={path.name:digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in ('.py','.md')}))
    print(json.dumps(dict(prepared=True,inputs=len(inputs))),flush=True)

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def bernstein(spline,index):
    width=float(spline.x[index+1]-spline.x[index])
    cubic,quadratic,linear,constant=spline.c[:,index]
    return [constant,constant+width*linear/3,
        constant+2*width*linear/3+width**2*quadratic/3,
        constant+width*linear+width**2*quadratic+width**3*cubic]

class Reference:
    def __init__(self,model,inputs):
        self.model=model
        self.system=parent.old.matched.System(model,4096,inputs)
        self.background=self.system.background
        self.basis=self.system.basis
        self.ladder=self.system.ladder
        self.emission=self.system.emission
        self.history_path=BRANCH/f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400/history.npz'
        self.history=load(inputs,self.history_path)
        assert len(self.history['expansion'])==6401
        assert float(self.history['heat'])==self.background.chi
        assert int(self.history['basis_count'])==96
        assert np.array_equal(self.history['temperature_template'],self.basis.temperature)
        assert np.array_equal(self.history['energy_row'],self.basis.energy)
        self.heat=mp.mpf(float(self.background.chi))
        self.mass_original=parent.matrix(self.basis.mass)
        self.mass=(self.mass_original+self.mass_original.T)/2
        self.factor,self.permutation=mp.mp.LU_decomp(self.mass)
        self.temperature=parent.matrix(self.basis.temperature[:,None])
        self.energy=parent.matrix(self.basis.energy[None,:])
        self.beta=mp.lu_solve(self.mass_original.T,self.energy.T).T
        self.defect_row=self.energy-self.temperature.T*self.mass
        self.defect=mp.sqrt((self.defect_row*self.solve(self.defect_row.T))[0])
        self.dc_constant=mp.mpf(float(self.emission.at.__globals__['integrated_dc'].DC_CONSTANT))
        self.compton=[parent.matrix(block[:96,:96]) for block in self.ladder.blocks]
        self.dc=parent.matrix(self.emission.nonlocal_matrix)
        self.br_values=[bernstein(self.emission.interpolator,index)
            for index in range(len(self.emission.interpolator.x)-1)]
        self.br={}
        self.reference_cache={}
        self.contraction_cache={}

    def solve(self,vector):
        return mp.mp.U_solve(self.factor,mp.mp.L_solve(self.factor,vector,self.permutation))

    def profile(self,coordinate):
        key=float(coordinate)
        if key not in self.reference_cache:
            points=self.history['expansion']
            index=int(np.clip(np.searchsorted(points,key,side='right')-1,0,len(points)-2))
            left,right=map(lambda value:mp.mpf(float(value)),points[index:index+2])
            fraction=(mp.mpf(key)-left)/(right-left)
            assert -mp.mpf('1e-12')<=fraction<=1+mp.mpf('1e-12')
            values=(1-fraction)*parent.matrix(self.history['profiles'][index,:,None])+fraction*parent.matrix(self.history['profiles'][index+1,:,None])
            gas=(1-fraction)*mp.mpf(float(self.history['temperature_scaled'][index]))+fraction*mp.mpf(float(self.history['temperature_scaled'][index+1]))
            self.reference_cache[key]=(values,gas)
        return self.reference_cache[key]

    def norm_and_pair(self,force):
        gas=-(self.beta*force)[0]
        squared=(force.T*self.solve(force))[0]+gas**2/self.heat
        assert squared>=0
        pair=((self.temperature.T-self.beta)*force)[0]
        return mp.sqrt(squared),abs(pair),gas

    def contract(self,kind,index,coordinate,control=0):
        key=(kind,index,control,float(coordinate))
        if key not in self.contraction_cache:
            values,gas=self.profile(coordinate)
            if kind=='br' and (index,control) not in self.br:
                self.br[index,control]=parent.matrix(self.br_values[index][control])
            matrix=self.compton[index] if kind=='compton' else self.dc if kind=='dc' else self.br[index,control]
            force=matrix*(values-self.temperature*gas)
            self.contraction_cache[key]=self.norm_and_pair(force)[:2]
        return self.contraction_cache[key]

    def actual(self,coordinate):
        local=self.background.at(float(coordinate))
        theta=local['thermal_parameter']
        rate=mp.mpf(float(local['coefficient']/theta))
        stiffness=parent.matrix(self.ladder.at(theta,0)[:96,:96]-self.emission.at(theta,'dcbr'))
        values,gas=self.profile(coordinate)
        force=rate*stiffness*(values-self.temperature*gas)
        norm,pair,gas_force=self.norm_and_pair(force)
        return dict(force=force,gas=gas_force,norm=norm,pair=pair,rate=rate,stiffness=stiffness,theta=theta,local=local)

    def pieces(self):
        theta_scale=self.background.theta0/self.background.start_scale
        values=[FIRST,LAST]
        values.extend(float(value) for value in self.history['expansion'] if FIRST<value<LAST)
        values.extend(math.log(theta_scale/float(value)) for value in self.ladder.temperatures if FIRST<math.log(theta_scale/float(value))<LAST)
        values.extend(math.log(theta_scale)-float(value) for value in self.emission.interpolator.x if FIRST<math.log(theta_scale)-float(value)<LAST)
        return sorted(set(values))

    def cell_bound(self,first,last):
        midpoint=(first+last)/2
        local=self.background.at(midpoint)
        theta=local['thermal_parameter']
        upper=int(np.clip(np.searchsorted(self.ladder.temperatures,theta),1,len(self.ladder.temperatures)-1))
        br_index=int(np.clip(np.searchsorted(self.emission.interpolator.x,math.log(theta),side='right')-1,0,len(self.br_values)-1))
        compton=[self.contract('compton',index,point) for index in (upper-1,upper) for point in (first,last)]
        dc=[self.contract('dc',0,point) for point in (first,last)]
        br=[self.contract('br',br_index,point,control) for control in range(4) for point in (first,last)]
        first_local=self.background.at(first)
        native=self.background.parent.at(first_local['moment'])
        rate_bound=mp.sqrt(3)*mp.mpf(float(self.background.parent.opacity_constant))/(
            mp.mpf(float(native['scale']))*mp.sqrt(mp.mpf(float(self.background.parent.radiation))))
        dc_scale=self.dc_constant*mp.mpf(float(first_local['thermal_parameter']))**2
        bound=[rate_bound*(max(value[part] for value in compton)+dc_scale*max(value[part] for value in dc)+max(value[part] for value in br)) for part in (0,1)]
        return dict(first=first,last=last,norm=bound[0],pair=bound[1],rate_bound=rate_bound,
            compton_nodes=[upper-1,upper],br_index=br_index)

if __name__=='__main__':
    parent.old.source.modest()
    prepare()

