from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_stable_current_20260930 import stable_density_rows
from annular_C0_stable_transport_identity_20260930 import stable_identity_rows
from annular_C0_transport_context_20260930 import restore
from annular_C0_transport_identity_20260930 import identity_rows
from probe_annular_C0_precise_transport_20260930 import precise_probe
from validate_annular_C0_boundaries_20260930 import toy_data,metric
from annular_C0_boundary_integral_20260930 import density_rows
from annular_C0_material_integral_v3_20260930 import material_density_rows
from mpmath import mp
from decimal import localcontext
from time import perf_counter
import argparse
import ctypes
import json
import numpy as np
import sympy as sp


def symbolic(evidence):
    alpha,alpha_r,alpha_t,beta,beta_r,speed,speed_r,temporal,temporal_t,gradient,rate_r,integral,profile,first,second=sp.symbols(
        'alpha alpha_r alpha_t beta beta_r W W_r T T_t g v_r I h S0 S1')
    momentum=(alpha_t+speed*alpha_r+speed_r*alpha)*temporal+alpha*temporal_t
    flux=alpha*speed*temporal+beta*gradient
    energy=(alpha*temporal**2+beta*gradient**2)/2
    energy_dot=((alpha_t+speed*alpha_r)*temporal**2+(-beta*alpha_t/alpha+speed*beta_r)*gradient**2)/2
    energy_dot+=alpha*temporal*temporal_t+beta*gradient*(rate_r-speed_r*gradient)
    old=-momentum*((temporal+speed*gradient)*integral-first)-flux*(rate_r*integral-second)
    old+=(energy_dot+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*profile
    remainder=-alpha*speed*temporal*rate_r-(speed*alpha_r+alpha*speed_r)*temporal**2/2
    remainder+=(speed*beta_r-beta*speed_r)*gradient**2/2
    new=momentum*(first-speed*gradient*integral)+flux*second+remainder*integral+energy*speed*profile
    evidence.check('symbolic_exact_current_reduction',sp.expand(old-new)==0)
    wrong=new-remainder*integral
    evidence.check('symbolic_omission_detected',sp.expand(old-wrong)!=0)
    radius=5.5+1.2*np.array([.07,.29,.63,.91])
    for branch in [0,1]:
        data=toy_data(radius,single=True)
        for amount in [0.,.003,-.004,1e-25j]:
            values,radial,time=metric(radius,branch,amount)
            for material in [False,True]:
                old_rows=(material_density_rows if material else density_rows)(data,radius,values,radial,time,amount)
                new_rows=stable_density_rows(data,radius,values,radial,time,amount,material=material)
                error=float(np.max(abs(new_rows-old_rows)))
                evidence.check(f'toy:{branch}:{amount}:{material}',error<2e-11,error)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--label',default='annular-C0-stable-current-validation-attempt01')
    args=parser.parse_args()
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),4):
        raise OSError('Cannot set one core')
    evidence=EvidenceRun(args.label,__file__)
    started,deadline=perf_counter(),perf_counter()+1400
    try:
        symbolic(evidence)
        evidence.own(evidence.root/'DERIVATION-20260930-C0-stable-current.md')
        mp.dps=96
        with localcontext() as context:
            context.prec=70
            for branch in ['reference-reference','MTS-primary']:
                evaluator=restore(evidence,branch,'fine',deadline)['evaluator']
                cells=np.unique(np.linspace(0,len(evaluator.widths)-1,37).astype(int))
                indices=np.repeat(cells,9)
                labels=np.tile(np.repeat([-.37,.03,.29],3),len(cells))
                local=np.tile([.13,.47,.83],3*len(cells))
                left=evaluator.geometry.geometry(evaluator.edges[indices],labels)[0]
                right=evaluator.geometry.geometry(evaluator.edges[indices+1],labels)[0]
                offsets=left+(right-left)*local
                packet,active=evaluator.packet(labels,offsets)
                old=identity_rows(evaluator,packet,offsets)
                stable=stable_identity_rows(evaluator,packet,offsets)
                scales=np.maximum.reduce([abs(old['material']),abs(old['eulerian']),abs(old['transport'])])
                relative=abs(old['defect'])/np.maximum(scales,1e-100)
                selected=np.unique(np.r_[np.linspace(0,len(offsets)-1,12).astype(int),np.argmax(relative,axis=1),np.argmax(abs(old['defect']),axis=1)])
                exact=precise_probe(evaluator,{key:value[selected] for key,value in packet.items()},offsets[selected])[-1]
                names=['eulerian','material','transport']
                old_errors=np.array([old[name][:,selected] for name in names])-exact['result']
                new_errors=np.array([stable[name][:,selected] for name in names])-exact['result']
                current_improvement=np.max(abs(old_errors[:,1:]))/max(np.max(abs(new_errors[:,1:])),1e-100)
                scale=np.maximum.reduce([abs(stable[name]) for name in names])
                new_relative=float(np.max(abs(stable['defect'])/np.maximum(scale,1e-100)))
                path=evidence.output/(branch+'-stable-probes.npz')
                np.savez_compressed(path,selected=selected,old_errors=old_errors,new_errors=new_errors,
                    stable_defect=stable['defect'],precise_derivatives=exact['result'],offsets=offsets,labels=labels)
                evidence.own(path,'outputs')
                evidence.check(branch+':active',active.all())
                evidence.check(branch+':precise_oracle',exact['relative']<1e-40,exact['relative'])
                evidence.check(branch+':pointwise_transport',new_relative<1e-10,new_relative)
                evidence.check(branch+':current_arithmetic_improves',current_improvement>10,float(current_improvement))
                summary=dict(branch=branch,relative_transport_error=new_relative,current_improvement=float(current_improvement),
                    old_errors=np.max(abs(old_errors),axis=2).tolist(),new_errors=np.max(abs(new_errors),axis=2).tolist(),
                    valid_for_claim=False)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary),flush=True)
        evidence.report.update(seconds=perf_counter()-started,full_integral_repeated=False,github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
