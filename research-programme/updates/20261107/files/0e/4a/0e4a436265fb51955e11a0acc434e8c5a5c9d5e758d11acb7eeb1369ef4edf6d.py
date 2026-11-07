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
from scipy import integrate, interpolate, optimize

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'curvature-through-heavy-onset-20261007'
SPECTRUM=BRANCH/'resolved-matter-spectrum-20261007'
MATCHING=BRANCH/'native-heavy-matching-20261007'
NATIVE=MATCHING/'native'
TABLES=BRANCH/'native-two-field-transfer-20261007/runs/backgrounds'
sys.path.insert(0,str(SPECTRUM))
import spectrum_common as inherited
from project_grid import projection
from analyze_spectrum import summary as spectrum_summary
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
camb=inherited.camb
previous=inherited.previous
START=previous.START
UNIT=previous.H0/previous.C_LIGHT


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'precision_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


class HeavyDensity:
    def __init__(self,source,omega_m):
        self.table=np.load(source)
        self.fraction=float(self.table['fraction'])
        self.target=omega_m*self.fraction
        self.mass=float(self.table['heavy_mass_mpc'])
        self.match=float(self.table['matching_scale']) if 'matching_scale' in self.table else None
        if self.fraction:
            self.phi=interpolate.CubicSpline(self.table['heavy_efold'],self.table['phi_h'])
            self.velocity=interpolate.CubicSpline(self.table['heavy_efold'],self.table['phidot_h'])

    def __call__(self,efold):
        nodes=np.asarray(efold)
        if not self.fraction:
            return np.zeros_like(nodes),np.zeros_like(nodes)
        final=math.log(self.match if self.match else .0004)
        clipped=np.clip(nodes,START,final)
        scale=np.exp(clipped)
        velocity=self.velocity(clipped)
        density=(velocity**2+(scale*self.mass*self.phi(clipped))**2)/(6*UNIT**2*scale**2)
        derivative=-velocity**2/(UNIT**2*scale**2)
        dust=self.target*np.exp(-3*nodes)
        if self.match:
            return np.where(nodes<final,density,dust),np.where(nodes<final,derivative,-3*dust)
        lower=math.log(.0003)
        coordinate=np.clip((nodes-lower)/(final-lower),0.,1.)
        weight=coordinate**3*(10-15*coordinate+6*coordinate**2)
        weight_n=30*coordinate**2*(1-coordinate)**2/(final-lower)
        blended=np.exp((1-weight)*np.log(density)+weight*np.log(dust))
        slope=(1-weight)*derivative/density-3*weight+weight_n*np.log(dust/density)
        return blended,blended*slope


class SlowSource:
    def __init__(self,source):
        self.source=source
        self.old=np.load(source)
        self.omega_m,self.mu=previous.inherited_parameters()
        self.heavy=HeavyDensity(source,self.omega_m)
        self.species=previous.StandardSpecies(self.omega_m,self.heavy.fraction)

    def coefficients(self,efold,normalized,amplitude):
        ratio,conditioned=normalized
        standard,pressure=self.species.values(efold)
        heavy,heavy_n=self.heavy(efold)
        potential=standard+heavy+self.mu**2*amplitude**2*ratio**2
        kinetic_numerator=self.mu**4*amplitude**2*conditioned**2
        expansion2=(potential+np.sqrt(potential**2+4*kinetic_numerator))/2
        velocity=self.mu**2*amplitude*conditioned/expansion2
        slope=(-1.5*(standard+pressure)+.5*heavy_n)/expansion2-3*velocity**2
        return expansion2,slope,velocity

    def solve(self,amplitude,rtol=3e-11):
        def equation(efold,state):
            expansion2,slope,velocity=self.coefficients(efold,state,amplitude)
            return [velocity/amplitude,(slope-3)*state[1]-state[0]]

        boundaries=[START,0.]
        if self.heavy.match:
            boundaries.insert(1,math.log(self.heavy.match))
        state=[1.,-.2]
        pieces=[]
        for lower,upper in zip(boundaries[:-1],boundaries[1:]):
            result=integrate.solve_ivp(equation,(lower,upper),state,method='DOP853',rtol=rtol,
                atol=rtol*.01,max_step=.04,dense_output=True)
            assert result.success,result.message
            pieces.append(result)
            state=result.y[:,-1]
        expansion2=self.coefficients(0.,state,amplitude)[0]
        return float(expansion2),pieces

    def shoot(self,rtol=3e-11):
        old_amplitude=float(self.old['phi_s'][0])/math.sqrt(6)
        history=[]
        def objective(amplitude):
            expansion,pieces=self.solve(amplitude,rtol)
            history.append(dict(amplitude=amplitude,flatness_residual=expansion-1,nfev=sum(piece.nfev for piece in pieces)))
            return expansion-1
        radius=.001*old_amplitude
        lower,upper=old_amplitude-radius,old_amplitude+radius
        left,right=objective(lower),objective(upper)
        assert left*right<0,'Inherited-amplitude neighbourhood no longer brackets the fixed flatness convention'
        amplitude=optimize.brentq(objective,lower,upper,xtol=5e-14,rtol=1e-14)
        expansion,pieces=self.solve(amplitude,rtol)
        return amplitude,pieces,expansion,history

    def sample(self,nodes,amplitude,pieces):
        result=np.empty((2,len(nodes)))
        for index,piece in enumerate(pieces):
            selected=(nodes>=piece.t[0])&(nodes<=piece.t[-1])
            result[:,selected]=piece.sol(nodes[selected])
        expansion2,_,velocity=self.coefficients(nodes,result,amplitude)
        return dict(phi_s=math.sqrt(6)*amplitude*result[0],
            phidot_s=math.sqrt(6)*np.exp(nodes)*UNIT*np.sqrt(expansion2)*velocity,
            expansion2=expansion2,conditioned_velocity=result[1])
