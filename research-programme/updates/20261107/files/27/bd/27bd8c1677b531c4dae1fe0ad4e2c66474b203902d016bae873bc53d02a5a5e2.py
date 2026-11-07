from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from derive_annular_native_shape_stress_20260928 import physical_data, nodal_transport
from annular_native_trial_matrix_20261001 import transport, image_and_tangent
from search_annular_native_shape_state_20261001 import pinned_movements
from probe_annular_nonzero_kernel_family_20261001 import nodal_radii,unit_profile
from decimal import Decimal,localcontext
from time import perf_counter
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-null-slice-preservation-gate-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+1800
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-null-slice-fourth-order-preservation.md')
        parent_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        construction_path = evidence.output.parent/'annular-nonzero-kernel-family-attempt02/status.json'
        construction = json.loads(construction_path.read_text())
        evidence.own(construction_path)
        evidence.check('construction_complete',construction['state']=='complete' and all(row['passed'] for row in construction['checks']))
        for category in ['inputs','outputs']:
            digests.update(construction[category])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed source '+relative)
        time,coefficient = sp.symbols('t C')
        expression = coefficient*time**4/4
        evidence.check('fourth_derivative_factor_six',sp.diff(expression,time,4)==6*coefficient)
        evidence.check('lower_derivatives_silent',all(sp.diff(expression,time,order).subs(time,0)==0 for order in range(4)))
        evidence.report.update(parent_physical_acceleration_computed=False,
            finite_curve_is_algebraic_oracle=True,github_action=False,subagents_used=False)
        with localcontext() as context:
            context.prec = 70
            for level in ['fine','third']:
                loads,action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                packet_path = evidence.root/sources['packet']
                evidence.own(packet_path)
                packet = json.loads(packet_path.read_text())
                engine = NativeKernel(action.mesh,packet['gram_support'],True)
                amplitude = Decimal(next(row for row in construction['cases'] if row['level']==level)['amplitude'])
                for label in [-.45,0.,.37]:
                    data = physical_data(engine,loads,action,label)
                    null = amplitude*unit_profile(nodal_radii(engine,data['edges']),data['edges'][0],data['source'],data['edges'][-1])
                    fields = np.column_stack([null,data['field']])
                    movements,pin_error = pinned_movements(engine,data['edges'],data['source'])
                    field_rates = transport(engine,data['edges'],fields,movements)
                    images,tangents = image_and_tangent(engine,data['edges'],fields,movements,field_rates)
                    evidence.check(level+':'+str(label)+':kernel_section_zero',maximum(images[:,0])<Decimal('1e-45'))
                    evidence.check(level+':'+str(label)+':complete_shape_tangent_zero',maximum(tangents[:,:,0])<Decimal('1e-40'),str(maximum(tangents[:,:,0])))
                    weights = np.asarray(engine.apply('sampling',data['beta']),float)
                    changed = data['beta_radial'][:,None]*movements[engine.native_edges]
                    changed_weights = engine.sampling@np.asarray(changed,float)
                    image,tangent = np.asarray(images,float),np.asarray(tangents,float)
                    product = np.einsum('ai,a,akj->kij',image,weights,tangent)
                    forms = (product+product.transpose(0,2,1))/2+np.einsum('ai,ak,aj->kij',image,changed_weights,image)/2
                    evidence.check(level+':'+str(label)+':quadratic_radical',float(np.max(abs(forms[:,:,0])))<1e-40)
                    perturbations = []
                    for time_value in [Decimal('0.125'),Decimal('0.0625')]:
                        trial = null+time_value**2*data['field']/2
                        actual = engine.evaluate(data['edges'],trial,data['beta'])
                        force = []
                        for test in range(13):
                            rate = nodal_transport(engine,actual,movements[:,test])
                            value = sum(actual['field_gradient']*rate,Decimal(0))+sum(actual['edge_gradient']*movements[:,test],Decimal(0))
                            value += sum(actual['load']*changed[:,test],Decimal(0))
                            force.append(float(value))
                        expected = float(time_value**4/4)*forms[:,1,1]
                        discrepancy = float(np.max(abs(np.array(force)-expected)/(1e-35+1e-11*abs(expected))))
                        evidence.check(level+':'+str(label)+':finite_curve:'+str(time_value),discrepancy<=1,discrepancy)
                        perturbations.append(dict(time=str(time_value),forces=force,expected=expected.tolist(),scaled_error=discrepancy))
                    large,small = np.array(perturbations[0]['forces']),np.array(perturbations[1]['forces'])
                    scaling_error = float(np.max(abs(large-16*small))/max(float(np.max(abs(large))),1e-40))
                    evidence.check(level+':'+str(label)+':fourth_order_scaling',scaling_error<1e-11,scaling_error)
                    path = evidence.output/(level+'-'+str(label)+'.npz')
                    np.savez_compressed(path,forms=forms,forces_large=large,forces_small=small,
                        null_image_max=np.array(str(maximum(images[:,0]))),
                        null_tangent_max=np.array(str(maximum(tangents[:,:,0]))))
                    evidence.own(path,'outputs')
                    evidence.report['cases'].append(dict(level=level,label=label,path=str(path.relative_to(evidence.root)),
                        radical_max=float(np.max(abs(forms[:,:,0]))),test_direction_force_max=float(np.max(abs(forms[:,1,1]))),
                        fourth_order_scaling_error=scaling_error,perturbations=perturbations))
                    evidence.save()
        evidence.report.update(seconds=perf_counter()-started,full_equilibrium_solved=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

