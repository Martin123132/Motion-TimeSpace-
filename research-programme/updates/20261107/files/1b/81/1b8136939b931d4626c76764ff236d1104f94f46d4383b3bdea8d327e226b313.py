from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from annular_quadratic_core_20261002 import core_basis,live_core,source_geometry,core_forms
from annular_source_flat_native_20261002 import movements
from annular_physical_native_kernel_20260928 import NativeKernel,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_zero_rate_euler_20261001 import zero_rate_system,endpoint_traction,direct_momentum_jacobian
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from probe_annular_native_carrier_v2_20261002 import carrier_field
from probe_annular_transmission_material_20261002 import point_covectors
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal,localcontext
from scipy.sparse import save_npz
from time import perf_counter
import ctypes
import gc
import json
import numpy as np


def two_parabolas(radius,native,values,left,right):
    interval = np.clip(np.searchsorted(native,radius,side='right')-1,0,len(native)-2)
    width = native[interval+1]-native[interval]
    coordinate = (radius-native[interval])/width
    first,last = values[interval],values[interval+1]
    outgoing,incoming = right[interval],left[interval+1]
    middle = 2*(last-first)/width-(outgoing+incoming)/2
    low = first+width*outgoing*coordinate+width*(middle-outgoing)*coordinate**2
    high = last-width*incoming*(1-coordinate)+width*(incoming-middle)*(1-coordinate)**2
    return np.where(coordinate<=Decimal('.5'),low,high)


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-live-native-transmission-third-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+5400
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-live-native-transmission-pilot.md')
        base = 'source-intake/navier-stokes/20260914/'
        carrier_report = verify_report(evidence,base+'annular-native-carrier-denominator-repair-attempt02/status.json')
        construction = verify_report(evidence,base+'annular-quadratic-core-state-third-attempt01/status.json')
        evidence.check('completed_candidate_sources',carrier_report['state']==construction['state']=='complete')
        evidence.check('sampled_carrier_candidate',all(row['sampled_nonzero_denominators'] for row in carrier_report['cases']))
        parent_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        for report in [carrier_report,construction]:
            for category in ['inputs','outputs']:
                digests.update(report[category])
        state = read_archive(evidence.root/construction['primary_state_path'])
        packet = json.loads((evidence.root/construction['packet_path']).read_text())
        epsilon = Decimal(carrier_report['epsilon'])
        ratios = state['ratios'].copy()
        amplitude = Decimal.from_float(construction['amplitude'])
        active_original = read_archive(evidence.root/next(row for row in carrier_report['cases'] if row['level']=='third')['path'])['active']
        with localcontext() as context:
            context.prec = 64
            unused,old_action,sources = restore_case(evidence,digests,'MTS-primary','third',deadline)
            loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
        owner = action.owner
        coordinates = loads.coordinates.copy()
        rates = loads.rates.copy()
        engine = NativeKernel(action.mesh,packet['gram_support'],True)
        evidence.report.update(iterations=[],results=[],states=[],epsilon=str(epsilon),packet_path=construction['packet_path'],
            source_acceleration_fitted=False,physical_evolution=False,github_action=False,subagents_used=False)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe live-transmission stage boundary')
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        def solve(current_loads,current_action,branch,name,spatial,material,oracle=False):
            progress(name+':Hessian')
            system = zero_rate_system(current_action,spatial,material,deadline,lambda stage:progress(name+':'+stage))
            native_engine = NativeKernel(current_action.mesh,packet['gram_support'],branch=='primary')
            points,weights = np.polynomial.legendre.leggauss(material)
            points,weights = points/2,weights/2
            weights *= 6*(points+.5)*(.5-points)
            native_force = np.zeros_like(system['force'])
            energy_rows,force_rows,jump_errors,jump_scales,point_errors,point_scales,slopes,curvatures = [],[],[],[],[],[],[],[]
            interpolation_error = 0.
            with localcontext() as context:
                context.prec = 64
                for count,(label,weight) in enumerate(zip(points,weights)):
                    data = physical_data(native_engine,current_loads,current_action,label)
                    result = native_engine.evaluate(data['edges'],data['field'],data['beta'])
                    source_force = sum(result['edge_gradient']*data['displacement'],Decimal(0))
                    source_force += sum(result['load']*data['beta_radial']*data['displacement'][native_engine.native_edges],Decimal(0))
                    native_force -= weight*np.outer(data['cardinal'],np.r_[np.asarray(result['field_gradient'],float),float(source_force)])
                    energy_rows.append(float(result['energy']))
                    force_rows.append(core_forms(native_engine,data,data['field'][:,None],movements(native_engine,data['edges'],data['source']))[0][:,0,0])
                    atom = result['atoms']
                    selected = native_engine.native_edges[1:-1]
                    indices = np.r_[native_engine.indices[:,0],native_engine.indices[-1,2]][native_engine.native_edges][1:-1]
                    before,after = atom['slope_right'][selected-1],atom['slope_left'][selected]
                    field_load = result['field_gradient'][indices]
                    shape_load = result['edge_gradient'][selected]+result['load'][1:-1]*data['beta_radial'][1:-1]
                    point = field_load*(before+after)/2+shape_load
                    jump = data['beta'][1:-1]*(after-before)-field_load
                    jump_errors.append(float(maximum(jump)))
                    jump_scales.append(float(maximum(field_load)))
                    point_errors.append(float(maximum(point)))
                    point_scales.append(float(maximum(abs(field_load*(before+after)/2)+abs(shape_load))))
                    slopes.append([float(atom['slope_right'][native_engine.anchor-1]),float(atom['slope_left'][native_engine.anchor])])
                    curvatures.append([float(atom['second'][native_engine.anchor-1]),float(atom['second'][native_engine.anchor])])
                    approximate = np.polynomial.chebyshev.chebval(2*label,current_loads.native_factor_coefficients)
                    interpolation_error = max(interpolation_error,float(np.max(abs(approximate-np.asarray(result['image'],float)))/max(float(maximum(result['image'])),1e-30)))
                    if count%16==15:
                        progress(name+':native layer '+str(count+1))
            force = system['force']+native_force
            acceleration = system['inverse'].solve(force.ravel()).reshape(force.shape)
            for repeat in range(2):
                residual = (system['matrix']@acceleration.ravel()).reshape(force.shape)-force
                acceleration -= system['inverse'].solve(residual.ravel()).reshape(force.shape)
            residual = (system['matrix']@acceleration.ravel()).reshape(force.shape)-force
            relative = float(system['inverse'].residual_norm(residual)/system['inverse'].residual_norm(force))
            evidence.check(name+':complete_Euler',relative<2e-11,relative)
            evidence.check(name+':factor_interpolation',interpolation_error<2e-8,interpolation_error)
            boundary = endpoint_traction(current_action,material)
            evidence.check(name+':outer_flux',not np.any(boundary))
            radial_nodes = current_action.solver.nodes
            beta = radial_nodes**2*np.exp(current_action.solution['state'][1])*np.sqrt(1-2*current_action.solution['state'][0]/radial_nodes)
            radial_energy = float(current_action.solver.integrated(beta.ravel()*current_action.solver.fields['gram'][branch])[-1,-1])
            native_energy = float(weights@np.array(energy_rows))
            energy_error = abs(native_energy-radial_energy)/max(abs(native_energy),1e-30)
            evidence.check(name+':native_energy_closure',energy_error<2e-8,energy_error)
            if oracle:
                direction = np.zeros_like(acceleration)
                direction[:,:-1] = .01*np.sin(current_action.knots)[None,:]
                direction[:,-1] = .02
                direct = direct_momentum_jacobian(current_action,direction,spatial,material,deadline)
                expected = (system['matrix']@direction.ravel()).reshape(direction.shape)
                error = float(np.max(abs(direct-expected))/max(np.max(abs(expected)),1e-30))
                evidence.check(name+':momentum_Jacobian',error<2e-11,error)
            cardinal,speed,drift = source_geometry(current_action,points)
            source_acceleration = cardinal@acceleration[:,-1]
            slopes,curvatures = np.array(slopes),np.array(curvatures)
            trace = speed[:,None]*curvatures+(drift+source_acceleration)[:,None]*slopes
            matrix_path = evidence.output/(name+'-mass.npz')
            save_npz(matrix_path,system['matrix'])
            evidence.own(matrix_path,'outputs')
            saved_path = save(name+'-acceleration',acceleration=acceleration,force=force,native_force=native_force,
                wave_source_force=system['force'],residual=residual,coordinates=np.asarray(current_loads.coordinates,str),rates=current_loads.rates,
                labels=points,weights=weights,slopes=slopes,curvatures=curvatures,trace=trace,speed_square=speed,drift=drift,
                source_acceleration=source_acceleration,native_energy_layers=energy_rows,shape_layers=force_rows,
                jump_errors=jump_errors,jump_scales=jump_scales,point_errors=point_errors,point_scales=point_scales,boundary_force=boundary)
            item = dict(name=name,branch=branch,material=material,spatial=spatial,path=saved_path,matrix_path=str(matrix_path.relative_to(evidence.root)),
                Euler_relative=relative,maximum_trace_residual=float(np.max(abs(trace))),maximum_acceleration=float(np.max(abs(acceleration))),
                maximum_shape_force=float(np.max(abs(np.array(force_rows)))),integrated_shape_force_max=float(np.max(abs(weights@np.array(force_rows)))),
                native_energy=native_energy,maximum_point_residual=max(point_errors),relative_point_residual=max(point_errors)/max(max(point_scales),1e-30),
                maximum_jump_residual=max(jump_errors),relative_jump_residual=max(jump_errors)/max(max(jump_scales),1e-30),valid_for_claim=False)
            evidence.report['results'].append(item)
            evidence.save()
            del system
            gc.collect()
            return acceleration,item
        converged = False
        for iteration in range(4):
            progress('build live iteration '+str(iteration))
            with localcontext() as context:
                context.prec = 64
                raw = core_basis(owner,engine,coordinates[:,-1],ratios)[:,:,0]*amplitude
                value_error,jet_error,alignment_error = Decimal(0),Decimal(0),Decimal(0)
                minimum_margin = 1.
                for index,label in enumerate(owner.layer_rule.points/2):
                    data = physical_data(engine,loads,action,label)
                    data['field'] = raw[:,index]
                    original = point_covectors(engine,data)
                    carrier,unused,active = carrier_field(engine,data)
                    active |= active_original
                    response = point_covectors(engine,dict(data,field=carrier))
                    row = point_covectors(engine,dict(data,field=data['field']+epsilon*carrier))
                    ratio = float(maximum(original['field'][active]/(epsilon*response['field'][active])))
                    minimum_margin = min(minimum_margin,1-ratio)
                    target = row['mean'].copy()
                    for selected in np.flatnonzero(active):
                        if row['field'][selected]==0:
                            raise RuntimeError('Actual zero denominator; no floor permitted')
                        target[selected] = -row['shape'][selected]/row['field'][selected]
                    left,right = target-row['field']/(2*row['beta']),target+row['field']/(2*row['beta'])
                    radius = nodal_radii(engine,data['edges'])
                    field = two_parabolas(radius,row['native'],row['values'],left,right)
                    coordinates[index,:-1] = field
                    native_indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
                    value_error = max(value_error,maximum(field[native_indices]-row['values']))
                    atoms = engine.atoms(data['edges'],field)
                    native_selected = engine.native_edges[1:-1]
                    jet_error = max(jet_error,maximum(atoms['slope_right'][native_selected-1]-left[1:-1]),maximum(atoms['slope_left'][native_selected]-right[1:-1]))
                    for native_index in np.flatnonzero(active[:-1]|active[1:]):
                        middle = (row['native'][native_index]+row['native'][native_index+1])/2
                        alignment_error = max(alignment_error,min(abs(data['edges']-middle)))
                evidence.check('iteration'+str(iteration)+':native_values_exact',value_error<Decimal('1e-30'),str(value_error))
                evidence.check('iteration'+str(iteration)+':represented_one_sided_jets',jet_error<Decimal('1e-26'),str(jet_error))
                evidence.check('iteration'+str(iteration)+':half_interval_edges',alignment_error<Decimal('1e-28'),str(alignment_error))
                evidence.check('iteration'+str(iteration)+':positive_vertex_denominator_margin',minimum_margin>0,minimum_margin)
            loads,action = live_core(owner,coordinates,rates,packet['mesh'],packet,'primary',deadline)
            radial_residual = float(np.max(abs(action.solver.residual(action.solution['state'],'primary'))))
            evidence.check('iteration'+str(iteration)+':fresh_radial_equations',radial_residual<8e-14,radial_residual)
            state_path = save('iteration'+str(iteration)+'-state',coordinates=np.asarray(coordinates,str),rates=rates,edges=action.solver.edges,ratios=ratios,**action.solution)
            evidence.report['states'].append(dict(name='iteration'+str(iteration),branch='primary',path=state_path))
            acceleration,item = solve(loads,action,'primary','iteration'+str(iteration),12,48)
            cardinal,speed,drift = source_geometry(action,owner.layer_rule.points/2)
            updated = -(drift+cardinal@acceleration[:,-1])/speed
            evidence.report['iterations'].append(dict(iteration=iteration,ratio_update=float(np.max(abs(updated-ratios))),
                source_trace=item['maximum_trace_residual'],point_relative=item['relative_point_residual'],jump_relative=item['relative_jump_residual'],
                radial_residual=radial_residual,minimum_vertex_margin=minimum_margin))
            evidence.save()
            if item['maximum_trace_residual']<1e-9 and item['relative_point_residual']<1e-8 and item['relative_jump_residual']<1e-7:
                converged = True
                break
            ratios = updated
        high_acceleration,high = solve(loads,action,'primary','primary-16-64',16,64,True)
        reference_loads,reference_action = live_core(owner,coordinates,rates,packet['mesh'],packet,'reference',deadline)
        reference_path = save('reference-state',coordinates=np.asarray(coordinates,str),rates=rates,edges=reference_action.solver.edges,**reference_action.solution)
        evidence.report['states'].append(dict(name='reference',branch='reference',path=reference_path))
        for spatial,material in [(12,48),(16,64)]:
            solve(reference_loads,reference_action,'reference','reference-'+str(spatial)+'-'+str(material),spatial,material,material==64)
        evidence.report.update(seconds=perf_counter()-started,vertex_iteration_converged=converged,
            heldout_initial_conditions_within_declared_tolerance=converged and high['maximum_trace_residual']<1e-9 and high['relative_point_residual']<1e-8 and high['relative_jump_residual']<1e-7,
            continuous_material_bound_proven=False,spatial_refinement_done_for_this_state=False,second_order_preservation_done=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
