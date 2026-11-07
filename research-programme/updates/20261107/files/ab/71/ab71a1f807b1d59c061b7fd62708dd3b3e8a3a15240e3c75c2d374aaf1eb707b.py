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
from scipy import interpolate,integrate,special

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'einstein-constraints-and-kinetic-response-20261007'
HISTORY=BRANCH/'full-history-source-precision-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
sys.path.insert(0,str(PARENT))
import constraint_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
camb=inherited.camb


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'collision_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def angular_grid(polar=24,azimuthal=48):
    cosine,weights=np.polynomial.legendre.leggauss(polar)
    angles=2*np.pi*np.arange(azimuthal)/azimuthal
    directions=np.stack([np.repeat(np.sqrt(1-cosine**2),azimuthal)*np.tile(np.cos(angles),polar),
        np.repeat(np.sqrt(1-cosine**2),azimuthal)*np.tile(np.sin(angles),polar),np.repeat(cosine,azimuthal)],axis=1)
    return directions,np.repeat(weights/(2*azimuthal),azimuthal)


def screens(directions):
    return np.eye(3)-np.einsum('ni,nj->nij',directions,directions)


def mean_matrix(weights,matrices):
    return np.einsum('n,nij->ij',weights,matrices)


def radiation_stress(directions,weights,intensity):
    scalar=np.trace(intensity,axis1=1,axis2=2)
    stress=np.empty((4,4),dtype=intensity.dtype)
    stress[0,0]=weights@scalar
    stress[0,1:]=stress[1:,0]=np.einsum('n,ni->i',weights*scalar,directions)
    stress[1:,1:]=np.einsum('n,ni,nj->ij',weights*scalar,directions,directions)
    return stress


def exact_collision(directions,weights,intensity,velocity,density=1.):
    screen=screens(directions)
    speed2=float(velocity@velocity)
    gamma=1/math.sqrt(1-speed2)
    projected=directions@velocity
    doppler=gamma*(1-projected)
    rest_direction=(directions+(gamma**2/(gamma+1)*projected-gamma)[:,None]*velocity)/doppler[:,None]
    rotation=(np.eye(3)+gamma**2/(gamma+1)*np.outer(velocity,velocity)+gamma*np.einsum('ni,j->nij',rest_direction,velocity))@screen
    rest_mean=mean_matrix(weights,doppler[:,None,None]**2*(rotation@intensity@np.swapaxes(rotation,1,2)))
    gain=1.5*doppler[:,None,None]**-3*(np.swapaxes(rotation,1,2)@rest_mean@rotation)
    return density*(gain-doppler[:,None,None]*intensity)


def taylor_collision(directions,weights,zeroth,first,second,velocity1,velocity2,density1,density2):
    screen=screens(directions)
    projected1=directions@velocity1
    projected2=directions@velocity2
    speed2=float(velocity1@velocity1)
    rotation1=np.einsum('ni,j->nij',directions,velocity1)@screen
    rotation2=(projected1[:,None,None]*np.einsum('ni,j->nij',directions,velocity1)-.5*np.outer(velocity1,velocity1)+np.einsum('ni,j->nij',directions,velocity2))@screen
    trans1=np.swapaxes(rotation1,1,2)
    trans2=np.swapaxes(rotation2,1,2)
    mean0=mean_matrix(weights,zeroth)
    moving1=first+rotation1@zeroth+zeroth@trans1
    mean1=mean_matrix(weights,moving1-2*projected1[:,None,None]*zeroth)
    moving2=second+rotation1@first+first@trans1+rotation2@zeroth+zeroth@trans2+rotation1@zeroth@trans1
    mean2=mean_matrix(weights,moving2-2*projected1[:,None,None]*moving1+(projected1**2+speed2-2*projected2)[:,None,None]*zeroth)
    gain0=1.5*(screen@mean0@screen)
    gain1_without_doppler=1.5*(screen@mean1@screen+trans1@mean0@screen+screen@mean0@rotation1)
    gain1=gain1_without_doppler+3*projected1[:,None,None]*gain0
    gain2=1.5*(screen@mean2@screen+trans1@mean1@screen+screen@mean1@rotation1+trans2@mean0@screen+screen@mean0@rotation2+trans1@mean0@rotation1)
    gain2+=3*projected1[:,None,None]*gain1_without_doppler+(6*projected1**2-1.5*speed2+3*projected2)[:,None,None]*gain0
    collision0=gain0-zeroth
    collision1=gain1-first+projected1[:,None,None]*zeroth
    collision2=gain2-second+projected1[:,None,None]*first-(.5*speed2-projected2)[:,None,None]*zeroth
    return collision0,collision1+density1*collision0,collision2+density1*collision1+density2*collision0


class CollisionProjectors:
    def __init__(self,polar=16,azimuthal=8):
        self.directions,self.weights=angular_grid(polar,azimuthal)
        self.screen=screens(self.directions)

    def parts(self,intensity,baryon_velocity,ratio):
        mean=mean_matrix(self.weights,intensity)
        isotropic=np.eye(3)*np.trace(mean)/3
        symmetric=(mean+mean.T)/2-isotropic
        antisymmetric=(mean-mean.T)/2
        radiation_iso=1.5*(self.screen@isotropic@self.screen)
        radiation_symmetric=(15/7)*(self.screen@symmetric@self.screen)
        radiation_antisymmetric=3*(self.screen@antisymmetric@self.screen)
        scalar=np.trace(intensity,axis1=1,axis2=2)
        photon_velocity=.75*np.einsum('n,ni->i',self.weights*scalar,self.directions)
        common=(photon_velocity+ratio*baryon_velocity)/(1+ratio)
        relative=photon_velocity-baryon_velocity
        dipole=2*(self.directions@photon_velocity)[:,None,None]*self.screen
        radiation_common=2*(self.directions@common)[:,None,None]*self.screen
        radiation_relative=2*(self.directions@(ratio*relative/(1+ratio)))[:,None,None]*self.screen
        fast=intensity-radiation_iso-radiation_symmetric-radiation_antisymmetric-dipole
        return [radiation_iso+radiation_common,fast,radiation_symmetric,radiation_antisymmetric,radiation_relative],common,-relative/(1+ratio)

    def apply(self,intensity,baryon_velocity,ratio,optical_depth,kind='exp'):
        rates=np.array([0.,-optical_depth,-.3*optical_depth,-.5*optical_depth,-optical_depth*(1+1/ratio)])
        if kind=='exp':
            coefficients=np.exp(rates)
        elif kind=='phi1':
            coefficients=special.exprel(rates)
        elif kind=='phi2':
            coefficients=np.empty_like(rates)
            small=abs(rates)<1e-4
            coefficients[small]=.5+rates[small]/6+rates[small]**2/24+rates[small]**3/120
            coefficients[~small]=(special.exprel(rates[~small])-1)/rates[~small]
        else:
            raise ValueError(kind)
        parts,common,relative=self.parts(intensity,baryon_velocity,ratio)
        radiation=sum(coefficient*part for coefficient,part in zip(coefficients,parts))
        velocity=coefficients[0]*common+coefficients[-1]*relative
        return radiation,velocity
