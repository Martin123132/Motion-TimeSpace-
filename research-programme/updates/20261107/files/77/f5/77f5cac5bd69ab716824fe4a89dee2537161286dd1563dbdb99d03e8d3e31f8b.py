from common import *
from source_adapter import native_background,other_density
from thermal_candidate import Thermal,parameters,FERMI,PANELS
from scipy.integrate import quad
import numpy as np


def main():
    modest()
    check_parent()
    require(read(ROOT/'density-diagnosis/result.json')['state']=='diagnosis_only_no_retry','diagnosed failure')
    destination=ROOT/'thermal-qualification'
    destination.mkdir(exist_ok=False)
    target=read(ROOT/'inventory/cold-target.json')
    source=NATIVE/'fortran/massive_neutrinos.f90'
    write(destination/'protocol.json',dict(source_files={str(source):digest(source),str(NATIVE/'fortran/results.f90'):digest(NATIVE/'fortran/results.f90')},candidate_sources=frozen_sources(),panels=PANELS,orders=[32,48,64],primary_order=48,cold_target=target,failed_inventory_preserved=True))
    reports=[]
    for model in ('heavy','cold'):
        native=native_background(model)
        params=parameters(native)
        accepted=load(BACKGROUND/'runs'/model/'dop-half-cap.npz')
        initial=accepted['a'][0]
        corner_scales=[switch/mass for mass in params['masses'] for switch in (.3+70/1399*1.01,63)]
        corners=np.asarray(corner_scales)[:,None]*np.exp(np.asarray([-.002,-.0005,-1e-8,0,1e-8,.0005,.002]))
        scales=np.unique(np.concatenate([np.exp(np.linspace(np.log(initial),np.log(target['scale_end']),513)),corners.ravel(),[initial,target['scale_start'],target['scale_end']]]))
        scales=scales[(scales>=initial)&(scales<=target['scale_end'])]
        efold=np.log(scales)
        write(destination/(model+'-parameters.json'),dict(parameters=params,initial_scale=float(initial),corner_scales=corner_scales,accepted_background=str(BACKGROUND/'runs'/model/'dop-half-cap.npz'),accepted_sha256=digest(BACKGROUND/'runs'/model/'dop-half-cap.npz')))
        packets={order:Thermal(params,order).values(efold) for order in (32,48,64)}
        refinement={str(order):float(np.max(abs(packets[order]-packets[64])/np.abs(packets[64]))) for order in (32,48)}
        require(max(refinement.values())<GATE,'direct thermal quadrature refinement')
        values=packets[48]
        require(np.all(values[:,0]>0),'positive physical density')
        require(np.all(values[:,1]/values[:,0]>=-2-ALGEBRA) and np.all(values[:,1]/values[:,0]<=-1+ALGEBRA),'analytic slope identity')
        require(np.all(values[:,2]/values[:,0]>=1-ALGEBRA) and np.all(values[:,2]/values[:,0]<=4+ALGEBRA),'analytic curvature identity')
        selected=np.unique(np.concatenate([np.linspace(0,len(scales)-1,17,dtype=int),[int(np.argmin(abs(scales-corner))) for corner in corner_scales]]))
        independent=[]
        for index in selected:
            scale=scales[index]
            total=np.array([(params['cdm']+params['baryon'])/scale+(params['photon']+params['massless'])/scale**2,
                            -(params['cdm']+params['baryon'])/scale-2*(params['photon']+params['massless'])/scale**2,
                            (params['cdm']+params['baryon'])/scale+4*(params['photon']+params['massless'])/scale**2])
            errors=np.zeros(3)
            for mass,coefficient in zip(params['masses'],params['coefficients']):
                for derivative in range(3):
                    def integrand(momentum):
                        energy=np.sqrt(momentum**2+(scale*mass)**2)
                        speed2=(momentum/energy)**2
                        factor=(1,-1-speed2,1+4*speed2-speed2**2)[derivative]
                        return momentum**2*energy*np.exp(-momentum)/(1+np.exp(-momentum))*factor/FERMI
                    value,error=quad(integrand,0,90,epsrel=2e-12,epsabs=1e-12,limit=250,points=[.1,1,3,10,30])
                    total[derivative]+=coefficient/scale**2*value
                    errors[derivative]+=coefficient/scale**2*error
            discrepancy=float(np.max(abs(total-values[index])/abs(total)))
            require(discrepancy<GATE,'independent adaptive thermal integral')
            independent.append(dict(index=int(index),scale=float(scale),relative_discrepancy=discrepancy,reported_integrator_relative_error=float(np.max(errors/abs(total)))))
        legacy=other_density(native,scales)
        legacy_error=float(np.max(abs(legacy-values[:,0])/values[:,0]))
        require(legacy_error<GATE,'candidate changes source value beyond retained numerical gate')
        thermal=Thermal(params)
        tail=thermal.tail_bounds(efold)
        tail_error=float(np.max(tail/abs(values)))
        require(tail_error<ALGEBRA,'analytic thermal tail')
        initial_external=float(thermal.values([np.log(initial)])[0,0])
        initial_rho=(accepted['velocities'][0]**2+(initial*accepted['masses']*accepted['fields'][0])**2)/2
        initial_hubble=float(np.sqrt((initial_external+initial_rho.sum())/3))
        hubble_change=float(initial_hubble/accepted['H'][0]-1)
        require(abs(hubble_change)<GATE,'initial Friedmann source correction')
        report=dict(model=model,parameters=params,quadrature_refinement=refinement,independent_checks=independent,max_legacy_density_relative_difference=legacy_error,
                    analytic_tail_relative_bound=tail_error,initial_hubble=initial_hubble,initial_hubble_relative_change=hubble_change,
                    curvature_range=[float(np.min(values[:,2]/values[:,0])),float(np.max(values[:,2]/values[:,0]))],corner_scales=corner_scales,
                    original_source_untouched=True,original_inventory_pass=False)
        np.savez_compressed(destination/(model+'-qualified.npz'),efold=efold,primary=values,coarse=packets[32],fine=packets[64],legacy=legacy,tail_bounds=tail)
        write(destination/(model+'-result.json'),report)
        reports.append(report)
        print(model,'legacy difference',legacy_error,'refinement',refinement,'H0 correction',hubble_change,flush=True)
    check_parent()
    write(destination/'result.json',dict(state='qualified_separate_thermal_candidate',passed=True,reports=reports,formal_interval_certificate=False,source_hashes=frozen_sources()))


if __name__=='__main__':
    main()
