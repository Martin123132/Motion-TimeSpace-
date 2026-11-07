from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_zero_rate_euler_20261001 import zero_rate_system,endpoint_traction,direct_momentum_jacobian
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from derive_annular_native_shape_stress_20260928 import physical_data,nodal_transport
from annular_native_trial_matrix_20261001 import transport,image_and_tangent
from search_annular_native_shape_state_20261001 import pinned_movements
from probe_annular_nonzero_kernel_family_20261001 import nodal_radii,unit_profile
from annular_mixed_weak_maps_20260920 import MixedMap
from decimal import Decimal,localcontext
from scipy.sparse import csr_matrix,save_npz
from copy import copy
from time import perf_counter
import argparse
import ctypes
import gc
import hashlib
import json
import numpy as np
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--max-seconds',type=float,default=7200)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-native-null-coupled-acceleration.md')
        evidence.own(evidence.root/'scripts/annular_zero_rate_euler_20261001.py')
        parent_path = evidence.output.parent/'annular-constrained-state-search-integrity-20261001.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('complete_parent_seal',parent['state']=='complete' and not parent['mismatches'])
        digests = parent['hashes']
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed source '+relative)
        def read(relative):
            path = (evidence.root/relative).resolve()
            if str(path.relative_to(evidence.root)) not in digests:
                raise RuntimeError('Unowned source '+relative)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {name:archive[name].copy() for name in archive.files}
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe stage boundary; completed outputs retained')
        speed,lapse,metric,mass = sp.symbols('V N F M',positive=True)
        dust_momentum = mass*speed/(metric*sp.sqrt(lapse**2-speed**2/metric))
        evidence.check('dust_zero_rate_inertia',sp.simplify(sp.diff(dust_momentum,speed).subs(speed,0)-mass/(metric*lapse))==0)
        evidence.check('dust_metric_derivative_zero',all(sp.diff(dust_momentum,variable).subs(speed,0)==0 for variable in [lapse,metric]))
        amplitude,source,lower,upper,fraction = sp.symbols('a b L U d')
        left = amplitude*(source-lower)**2*fraction*(fraction-1)
        right = amplitude*(upper-source)**2*fraction*(fraction-1)
        evidence.check('section_left_source_derivative',sp.simplify(sp.diff(left,source)-2*left/(source-lower))==0)
        evidence.check('section_right_source_derivative',sp.simplify(sp.diff(right,source)+2*right/(upper-source))==0)
        construction = read(str((evidence.output.parent/'annular-nonzero-kernel-family-attempt02/status.json').relative_to(evidence.root)))
        case = next(row for row in construction['cases'] if row['level']==args.level)
        state = read(case['initial_data_path'])
        progress('restore constructed time-symmetric slice')
        with localcontext() as context:
            context.prec = 64
            unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            packet = read(sources['packet'])
            loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
        evidence.check('all_configuration_rates_zero',not np.any(loads.rates))
        evidence.check('native_radial_authority',case['native_metric_residual']<8e-14)
        evidence.check('outer_field_nodes_retained',np.min(action.mesh['elements'][0])>=0 and np.min(action.mesh['elements'][-1])>=0)
        evidence.report.update(level=args.level,source_units='inherited_code_normalized',source_acceleration_fitted=False,
            independent_map_mass_added=False,full_coupled_zero_rate_reduction=True,
            outer_field_nodes_free=True,github_action=False,subagents_used=False,results=[])
        engine = NativeKernel(action.mesh,packet['gram_support'],True)
        amplitude_value = Decimal(case['amplitude'])
        for spatial_order,material_order in [(12,48),(16,64)]:
            prefix = str(spatial_order)+'-'+str(material_order)
            progress(prefix+':assemble coupled Hessian')
            system = zero_rate_system(action,spatial_order,material_order,deadline,lambda stage:progress(prefix+':'+stage))
            inverse,matrix,force = system['inverse'],system['matrix'],system['force']
            evidence.check(prefix+':zero_momentum_and_convection',not np.any(system['momentum'])
                and not np.any(system['action_momentum']) and not np.any(system['convection']))
            acceleration = system['acceleration'][0]
            for repeat in range(2):
                residual = (matrix@acceleration.ravel()).reshape(force.shape)-force
                acceleration -= inverse.solve(residual.ravel()).reshape(force.shape)
            residual = (matrix@acceleration.ravel()).reshape(force.shape)-force
            relative = inverse.residual_norm(residual)/inverse.residual_norm(force)
            correction = inverse.solve(residual.ravel()).reshape(force.shape)
            evidence.check(prefix+':coupled_Euler_residual',relative<2e-11 and np.max(abs(correction))<2e-10,
                dict(relative=relative,maximum_correction=float(np.max(abs(correction)))))
            direction = np.zeros_like(acceleration)
            direction[:,:-1] = .01*np.cos(action.owner.layer_rule.points[:,None])*np.sin(.7*action.knots[None,:])
            direction[:,-1] = .02+.003*action.owner.layer_rule.points
            direct = direct_momentum_jacobian(action,direction,spatial_order,material_order,deadline)
            predicted = (matrix@direction.ravel()).reshape(direction.shape)
            error = float(np.max(abs(direct-predicted))/max(np.max(abs(predicted)),1e-30))
            evidence.check(prefix+':independent_momentum_Jacobian',error<2e-11,error)
            reference = copy(action)
            reference.factor = MixedMap([],len(action.knots))
            reference.sampling = csr_matrix((0,len(action.knots)))
            reference.factor_values = np.zeros((0,len(action.source)))
            reference_result = reference.momentum_and_force(spatial_order,material_order,deadline)
            mismatch = float(np.max(abs(reference_result['force']-force)))
            evidence.check(prefix+':matched_reference_force',mismatch<2e-14*max(np.max(abs(force)),1e-20),mismatch)
            boundary_force = endpoint_traction(action,material_order)
            edge_acceleration = inverse.solve(boundary_force.ravel()).reshape(force.shape)
            bulk_acceleration = acceleration-edge_acceleration
            fixed_gram_effect = inverse.solve(system['fixed_reference_gram'].ravel()).reshape(force.shape)
            evidence.check(prefix+':fixed_reference_Gram_leakage',np.max(abs(fixed_gram_effect))<2e-10,float(np.max(abs(fixed_gram_effect))))
            matrix_path = evidence.output/(prefix+'-mass.npz')
            save_npz(matrix_path,matrix)
            evidence.own(matrix_path,'outputs')
            acceleration_path = save(prefix+'-acceleration',acceleration=acceleration,edge_acceleration=edge_acceleration,
                bulk_acceleration=bulk_acceleration,force=force,boundary_force=boundary_force,residual=residual,
                coordinates=np.asarray(loads.coordinates,str),rates=loads.rates,
                fixed_reference_Gram=system['fixed_reference_gram'],fixed_Gram_acceleration=fixed_gram_effect)
            evidence.report['last_acceleration'] = dict(path=acceleration_path,matrix_path=str(matrix_path.relative_to(evidence.root)))
            progress(prefix+':native quartic gates')
            labels,weights = np.polynomial.legendre.leggauss(material_order)
            labels,weights = labels/2,weights/2
            weights *= 6*(labels+.5)*(.5-labels)
            force_layers,baseline_leak = [],np.zeros_like(force)
            source_values,normal_max,edge_normal_max,bulk_normal_max = [],[],[],[]
            with localcontext() as context:
                context.prec = 64
                for label_index,label in enumerate(labels):
                    data = physical_data(engine,loads,action,label)
                    radius = nodal_radii(engine,data['edges'])
                    null = amplitude_value*unit_profile(radius,data['edges'][0],data['source'],data['edges'][-1])
                    section = np.array([2*value/(data['source']-data['edges'][0]) if point<data['source']
                        else -2*value/(data['edges'][-1]-data['source']) for point,value in zip(radius,null)],dtype=object)
                    movement,pin_error = pinned_movements(engine,data['edges'],data['source'])
                    columns = []
                    for member in [acceleration,edge_acceleration,bulk_acceleration]:
                        source_rate = Decimal.from_float(float(data['cardinal']@member[:,-1]))
                        field_rate = decimals(member[:,:-1].T)@decimals(data['cardinal'])
                        columns.append(field_rate-section*source_rate)
                    columns.append(decimals(acceleration[:,:-1].T)@decimals(data['cardinal']))
                    fields = np.column_stack(columns)
                    rates = transport(engine,data['edges'],fields,movement)
                    image,tangent = image_and_tangent(engine,data['edges'],fields,movement,rates)
                    coefficient = np.asarray(engine.apply('sampling',data['beta']),float)
                    native_coefficient = data['beta_radial'][:,None]*movement[engine.native_edges]
                    changed = engine.sampling@np.asarray(native_coefficient,float)
                    images,tangents = np.asarray(image,float),np.asarray(tangent,float)
                    work = np.einsum('ai,a,akj->kij',images,coefficient,tangents)
                    forms = (work+work.transpose(0,2,1))/2+np.einsum('ai,ak,aj->kij',images,changed,images)/2
                    force_layers.append(forms)
                    base = engine.evaluate(data['edges'],data['field'],data['beta'])
                    source_gradient = sum(base['edge_gradient']*data['displacement'],Decimal(0))
                    source_gradient += sum(base['load']*data['beta_radial']*data['displacement'][engine.native_edges],Decimal(0))
                    baseline_leak -= weights[label_index]*np.outer(data['cardinal'],np.r_[np.asarray(base['field_gradient'],float),float(source_gradient)])
                    source_values.append(float(data['cardinal']@acceleration[:,-1]))
                    normal_max.append(float(maximum(fields[:,0])))
                    edge_normal_max.append(float(maximum(fields[:,1])))
                    bulk_normal_max.append(float(maximum(fields[:,2])))
                    if label_index==len(labels)//2:
                        nodal_displacement = np.full(engine.count,Decimal(0),dtype=object)
                        for local,values in [(0,data['displacement'][:-1]),(1,(data['displacement'][:-1]+data['displacement'][1:])/2),(2,data['displacement'][1:])]:
                            selected = engine.indices[:,local]>=0
                            nodal_displacement[engine.indices[selected,local]] = values[selected]
                        endpoint = np.array([data['edges'][0] if point<data['source'] else data['edges'][-1] for point in radius],dtype=object)
                        alternative = amplitude_value*((2*radius-data['source']-endpoint)*nodal_displacement-(radius-endpoint))
                        evidence.check(prefix+':section_source_chain_rule',maximum(alternative-section)<Decimal('1e-45'))
                        scalar = engine.evaluate(data['edges'],fields[:,0],data['beta'])
                        direct_force = []
                        for test in range(13):
                            shifted = nodal_transport(engine,scalar,movement[:,test])
                            value = sum(scalar['field_gradient']*shifted,Decimal(0))
                            value += sum(scalar['edge_gradient']*movement[:,test],Decimal(0))
                            value += sum(scalar['load']*native_coefficient[:,test],Decimal(0))
                            direct_force.append(float(value))
                        error = float(np.max(abs(np.array(direct_force)-forms[:,0,0]))/max(np.max(abs(forms[:,0,0])),1e-30))
                        evidence.check(prefix+':independent_scalar_quartic_gate',error<2e-11,error)
                        disabled = NativeKernel(action.mesh,packet['gram_support'],False)
                        zero_images,zero_tangents = image_and_tangent(disabled,data['edges'],fields,movement,rates)
                        evidence.check(prefix+':reference_same_acceleration_zero_Gram_gate',maximum(zero_images)==0 and maximum(zero_tangents)==0)
                    if label_index%8==7 or label_index==len(labels)-1:
                        save(prefix+'-partial-gates',labels=labels[:label_index+1],weights=weights[:label_index+1],
                            force_layers=np.array(force_layers),source_acceleration=np.array(source_values))
                        progress(prefix+':material-label-'+str(label_index+1))
            total = np.einsum('l,lkij->kij',weights,np.array(force_layers))
            decomposition_error = float(np.max(abs(total[:,0,0]-total[:,1,1]-total[:,2,2]-2*total[:,1,2])))
            scale = max(float(np.max(abs(total))),1e-30)
            evidence.check(prefix+':boundary_bulk_cross_identity',decomposition_error<2e-11*scale,decomposition_error)
            leak_acceleration = inverse.solve(baseline_leak.ravel()).reshape(force.shape)
            evidence.check(prefix+':represented_native_leakage',np.max(abs(leak_acceleration))<2e-10,float(np.max(abs(leak_acceleration))))
            gate_path = save(prefix+'-gates',labels=labels,weights=weights,force_layers=np.array(force_layers),forms=total,
                fourth_derivative=6*total[:,0,0],full_coefficient=total[:,0,0]/4,source_acceleration=np.array(source_values),
                normal_max=np.array(normal_max),edge_normal_max=np.array(edge_normal_max),bulk_normal_max=np.array(bulk_normal_max),
                represented_native_force=baseline_leak,represented_native_acceleration=leak_acceleration)
            result = dict(spatial=spatial_order,material=material_order,acceleration_path=acceleration_path,gate_path=gate_path,
                matrix_path=str(matrix_path.relative_to(evidence.root)),maximum_acceleration=float(np.max(abs(acceleration))),
                maximum_source_acceleration=float(np.max(abs(acceleration[:,-1]))),source_acceleration_range=[min(source_values),max(source_values)],
                maximum_edge_acceleration=float(np.max(abs(edge_acceleration))),maximum_bulk_acceleration=float(np.max(abs(bulk_acceleration))),
                full_gate=total[:,0,0].tolist(),edge_gate=total[:,1,1].tolist(),bulk_gate=total[:,2,2].tolist(),
                edge_bulk_cross=(2*total[:,1,2]).tolist(),source_correction_omitted_gate=total[:,3,3].tolist(),
                fourth_derivative=(6*total[:,0,0]).tolist(),maximum_normal=max(normal_max),
                minimum_Schur_eigenvalue=inverse.minimum_schur_eigenvalue,minimum_field_pivot=inverse.minimum_field_cholesky_pivot,
                Euler_relative_residual=relative,momentum_oracle_relative_error=error,
                represented_native_leakage_acceleration=float(np.max(abs(leak_acceleration))),
                full_preservation_solved=False,outer_traction_retained=True)
            evidence.report['results'].append(result)
            evidence.save()
            del system,inverse,matrix
            gc.collect()
        low,high = evidence.report['results']
        low_data = np.load(evidence.root/low['acceleration_path'],allow_pickle=False)
        high_data = np.load(evidence.root/high['acceleration_path'],allow_pickle=False)
        acceleration_difference = high_data['acceleration']-low_data['acceleration']
        gate_difference = np.array(high['full_gate'])-np.array(low['full_gate'])
        evidence.report.update(seconds=perf_counter()-started,
            quadrature_acceleration_maximum_difference=float(np.max(abs(acceleration_difference))),
            quadrature_gate_maximum_difference=float(np.max(abs(gate_difference))),
            quadrature_gate_relative_difference=float(np.max(abs(gate_difference))/max(np.max(abs(high['full_gate'])),1e-30)),
            parent_native_Gram_constraint_gate_evaluated=True,physical_trajectory_computed=False)
        low_data.close()
        high_data.close()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

