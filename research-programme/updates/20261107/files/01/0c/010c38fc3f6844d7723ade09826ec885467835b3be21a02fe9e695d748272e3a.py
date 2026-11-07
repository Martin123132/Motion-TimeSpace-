from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_physical_native_kernel_20260928 import NativeKernel,maximum
from annular_quadratic_core_20261002 import core_forms
from annular_source_flat_native_20261002 import movements
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_moving_Legendre_current_20260921 import samples
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal,localcontext
from fractions import Fraction
from time import perf_counter
import ctypes
import json
import numpy as np


def hermite_values(radius,knots,values,left_slope,right_slope):
    interval = np.clip(np.searchsorted(knots,radius,side='right')-1,0,len(knots)-2)
    width = knots[interval+1]-knots[interval]
    coordinate = (radius-knots[interval])/width
    lower,upper = values[interval],values[interval+1]
    outgoing,incoming = right_slope[interval],left_slope[interval+1]
    field = (2*coordinate**3-3*coordinate**2+1)*lower+(coordinate**3-2*coordinate**2+coordinate)*width*outgoing
    field += (-2*coordinate**3+3*coordinate**2)*upper+(coordinate**3-coordinate**2)*width*incoming
    gradient = (6*coordinate**2-6*coordinate)*lower/width+(3*coordinate**2-4*coordinate+1)*outgoing
    gradient += (-6*coordinate**2+6*coordinate)*upper/width+(3*coordinate**2-2*coordinate)*incoming
    curvature = (12*coordinate-6)*lower/width**2+(6*coordinate-4)*outgoing/width
    curvature += (-12*coordinate+6)*upper/width**2+(6*coordinate-2)*incoming/width
    return field,gradient,curvature


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-interface-transmission-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-native-interface-transmission.md')
        parent_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        beta_control,load_control,shape_control = Fraction(7,5),Fraction(-3,8),Fraction(11,13)
        mean_control = -shape_control/load_control
        minus_control = mean_control-load_control/(2*beta_control)
        plus_control = mean_control+load_control/(2*beta_control)
        evidence.check('exact_field_transmission_sign',beta_control*(plus_control-minus_control)==load_control)
        evidence.check('exact_shape_pressure_sign',beta_control*(plus_control**2-minus_control**2)/2+shape_control==0)
        for level in ['fine','third']:
            relative = 'source-intake/navier-stokes/20260914/annular-quadratic-core-state-'+level+'-attempt01/status.json'
            construction = verify_report(evidence,relative)
            evidence.check(level+':construction_complete',construction['state']=='complete')
            for category in ['inputs','outputs']:
                digests.update(construction[category])
            state = read_archive(evidence.root/construction['primary_state_path'])
            packet = json.loads((evidence.root/construction['packet_path']).read_text())
            with localcontext() as context:
                context.prec = 64
                unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
                engine = NativeKernel(action.mesh,packet['gram_support'],True)
                data = physical_data(engine,loads,action,0.)
                result = engine.evaluate(data['edges'],data['field'],data['beta'])
                native = data['edges'][engine.native_edges]
                indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
                values = data['field'][indices]
                atom = result['atoms']
                edge_gradient = np.r_[atom['slope_left'][:1],(atom['slope_right'][:-1]+atom['slope_left'][1:])/2,atom['slope_right'][-1:]]
                mean = edge_gradient[engine.native_edges]
                field_load = result['field_gradient'][indices]
                shape_load = result['edge_gradient'][engine.native_edges]+result['load']*data['beta_radial']
                local_before = field_load*mean+shape_load
                movement = movements(engine,data['edges'],data['source'])
                forms = core_forms(engine,data,data['field'][:,None],movement)[0][:,0,0]
                point_before = np.asarray(local_before@movement[engine.native_edges],float)
                reduction_error = float(np.max(abs(point_before-forms))/max(np.max(abs(forms)),1e-30))
                evidence.check(level+':complete_shape_covector_reduction',reduction_error<2e-9,reduction_error)
                fraction = np.array([float(abs((point-data['source'])/((data['edges'][0] if point<data['source'] else data['edges'][-1])-data['source']))) for point in native])
                zone = np.where(fraction<=.18,0,np.where(fraction>=.82,np.where(np.asarray(native,float)<float(data['source']),1,2),3))
                kernel_active = np.array([not (np.all(zone[index:index+4]==0) or np.all(zone[index:index+4]==1) or np.all(zone[index:index+4]==2)) for index in range(len(native)-3)])
                image_active = np.asarray(abs(engine.template)@kernel_active.astype(float)>0).ravel()
                kernel_halo = np.asarray(abs(engine.template).T@image_active.astype(float)>0).ravel()
                active = np.asarray(abs(engine.sampling).T@image_active.astype(float)>0).ravel()
                for index in np.flatnonzero(kernel_halo):
                    active[index:index+4] = True
                target = mean.copy()
                singular = []
                for index in np.flatnonzero(active):
                    if field_load[index]==0:
                        if shape_load[index]!=0:
                            singular.append(int(index))
                    else:
                        target[index] = -shape_load[index]/field_load[index]
                left = target-field_load/(2*data['beta'])
                right = target+field_load/(2*data['beta'])
                local_after = field_load*target+shape_load
                jump_error = maximum(data['beta']*(right-left)-field_load)
                pressure_error = maximum(data['beta']*(right**2-left**2)/2+shape_load-local_after)
                evidence.check(level+':one_sided_field_jump_identity',jump_error<Decimal('1e-35'),str(jump_error))
                evidence.check(level+':one_sided_pressure_identity',pressure_error<Decimal('1e-35'),str(pressure_error))
                before_max,after_max = maximum(local_before),maximum(local_after)
                point_after = np.asarray(local_after@movement[engine.native_edges],float)
                archive = dict(radius=np.asarray(native,float),native_values=np.asarray(values,float),
                    native_values_exact=np.asarray(values,str),field_load_exact=np.asarray(field_load,str),shape_load_exact=np.asarray(shape_load,str),
                    beta_exact=np.asarray(data['beta'],str),mean_before_exact=np.asarray(mean,str),mean_target_exact=np.asarray(target,str),
                    left_exact=np.asarray(left,str),right_exact=np.asarray(right,str),active=active,
                    local_before_exact=np.asarray(local_before,str),local_after_exact=np.asarray(local_after,str),
                    weak_before=forms,weak_after=point_after)
                native_float,values_float = np.asarray(native,float),np.asarray(values,float)
                left_float,right_float = np.asarray(left,float),np.asarray(right,float)
                evidence.check(level+':finite_target_slopes',np.all(np.isfinite(left_float)) and np.all(np.isfinite(right_float)))
                evidence.check(level+':native_covers_endpoints',native[0]==data['edges'][0] and native[-1]==data['edges'][-1])
                beta_float = np.asarray(data['beta'],float)
                float_jump = beta_float*(right_float-left_float)-np.asarray(field_load,float)
                float_pressure = beta_float*(right_float**2-left_float**2)/2+np.asarray(shape_load,float)
                old_source = float(data['source'])
            integrals = []
            split = np.unique(np.r_[native_float,action.solver.edges])
            split = split[(split>=native_float[0])&(split<=native_float[-1])]
            for order in [16,24]:
                nodes,weights = np.polynomial.legendre.leggauss(order)
                radii = ((split[:-1]+split[1:])[:,None]+np.diff(split)[:,None]*nodes[None,:])/2
                measure = np.diff(split)[:,None]*weights[None,:]/2
                field,gradient,unused = hermite_values(radii.ravel(),native_float,values_float,left_float,right_float)
                metric_values,unused = action.solver.values(action.solution,radii.ravel())
                metric = 1-2*metric_values[0]/radii.ravel()
                speed = np.exp(metric_values[1])*np.sqrt(metric)
                beta = radii.ravel()**2*speed
                alpha = radii.ravel()**2/speed
                energy = float(measure.ravel()@(beta*gradient**2/2))
                norm = float(measure.ravel()@(alpha*field**2))
                old = samples(action,0.,order)
                old_energy = float(old['quadrature']['measure']@(old['geometry']['gradient']*old['gradient']**2/2))
                integrals.append(dict(order=order,wave_energy=energy,positive_norm=norm,old_wave_energy=old_energy,energy_ratio=energy/old_energy,
                    maximum_field=float(np.max(abs(field))),maximum_gradient=float(np.max(abs(gradient)))))
            energy_error = abs(integrals[1]['wave_energy']/integrals[0]['wave_energy']-1)
            evidence.check(level+':Hermite_energy_quadrature',energy_error<2e-8,energy_error)
            source_jet = [float(value[0]) for value in hermite_values(np.array([old_source]),native_float,values_float,left_float,right_float)]
            evidence.check(level+':source_pin_reconstruction',abs(source_jet[0])<1e-12,source_jet[0])
            evidence.check(level+':source_slope_retained',abs(source_jet[1]-construction['amplitude'])<1e-8,source_jet[1])
            path = evidence.output/(level+'-native-transmission.npz')
            np.savez_compressed(path,**archive)
            evidence.own(path,'outputs')
            row = dict(level=level,path=str(path.relative_to(evidence.root)),central_label_only=True,frozen_metric=True,
                singular_rows=singular,active_native_knots=int(np.count_nonzero(active)),
                minimum_active_abs_A=float(np.min(abs(field_load[active]))),maximum_abs_A=float(maximum(field_load)),
                maximum_old_gradient=float(maximum(mean)),maximum_target_gradient=float(maximum(target)),
                local_residual_before=float(before_max),local_residual_after=float(after_max),
                weak_residual_before=float(np.max(abs(forms))),weak_residual_after=float(np.max(abs(point_after))),
                inactive_residual=float(maximum(local_after[~active])),float_jump_residual=float(np.max(abs(float_jump))),
                float_pressure_residual=float(np.max(abs(float_pressure))),integrals=integrals,source_jet=source_jet,
                target_native_values_and_energy_retained=True,live_radial_solve_for_Hermite_done=False,
                all_material_labels_solved=False,physical_trajectory_computed=False,valid_for_claim=False)
            evidence.report['cases'].append(row)
            evidence.save()
        evidence.report.update(seconds=perf_counter()-started,point_interface_law_derived=True,global_state_solved=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
