from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_quadratic_core_20261002 import core_basis,live_core,source_geometry,core_forms,compensated_shapes
from annular_source_flat_native_20261002 import trial_norm,movements
from annular_native_trial_matrix_20261001 import transport,image_and_tangent
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from derive_annular_native_shape_stress_20260928 import physical_data,nodal_transport
from annular_zero_rate_euler_20261001 import zero_rate_system,endpoint_traction,direct_momentum_jacobian
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from decimal import Decimal,localcontext
from scipy.sparse import save_npz
from time import perf_counter
import argparse
import ctypes
import gc
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-quadratic-core-state-'+args.level+'-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+7200
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-quadratic-core-joint-attempt.md')
        seal_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(seal_path)
        parent = json.loads(seal_path.read_text())
        digests = parent['hashes']
        evidence.check('sealed_parent',parent['state']=='complete' and not parent['mismatches'])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe saved stage boundary')
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        flat_path = evidence.output.parent/('annular-source-flat-native-state-'+args.level+'-attempt02/status.json')
        evidence.own(flat_path)
        flat = json.loads(flat_path.read_text())
        with np.load(evidence.root/flat['states']['primary']['path'],allow_pickle=False) as archive:
            old_state = {name:archive[name].copy() for name in archive.files}
        old_result = next(row for row in flat['results'] if row['branch']=='primary' and row['material']==64)
        with np.load(evidence.root/old_result['acceleration_path'],allow_pickle=False) as archive:
            old_acceleration = archive['acceleration'].copy()
        with localcontext() as context:
            context.prec = 64
            unused,original_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            packet = json.loads((evidence.root/flat['packet_path']).read_text())
            old_loads,base_action = restore_refined(original_action.owner,old_state,packet['mesh'],packet,'primary',deadline)
            engine = NativeKernel(base_action.mesh,packet['gram_support'],True)
            labels = base_action.owner.layer_rule.points/2
            cardinal,speed_square,drift = source_geometry(base_action,labels)
            ratios = -(drift+cardinal@old_acceleration[:,-1])/speed_square
        evidence.report.update(level=args.level,packet_path=flat['packet_path'],sources=sources,iterations=[],results=[],
            source_acceleration_fitted=False,native_shape_constraints_solved=False,physical_trajectory_computed=False,
            github_action=False,subagents_used=False)

        def solve_case(loads,action,branch,name,spatial,material,oracle=False):
            progress(name+':Hessian')
            system = zero_rate_system(action,spatial,material,deadline,lambda stage:progress(name+':'+stage))
            matrix,inverse = system['matrix'],system['inverse']
            native_engine = NativeKernel(action.mesh,packet['gram_support'],branch=='primary')
            points,weights = np.polynomial.legendre.leggauss(material)
            points,weights = points/2,weights/2
            weights *= 6*(points+.5)*(.5-points)
            native_force = np.zeros_like(system['force'])
            energies,slopes,curvatures,core_gradients = [],[],[],[]
            interpolation_error,fast_image_error = 0.,0.
            with localcontext() as context:
                context.prec = 64
                for position,(label,weight) in enumerate(zip(points,weights)):
                    data = physical_data(native_engine,loads,action,label)
                    result = native_engine.evaluate(data['edges'],data['field'],data['beta'])
                    source_force = sum(result['edge_gradient']*data['displacement'],Decimal(0))
                    source_force += sum(result['load']*data['beta_radial']*data['displacement'][native_engine.native_edges],Decimal(0))
                    native_force -= weight*np.outer(data['cardinal'],np.r_[np.asarray(result['field_gradient'],float),float(source_force)])
                    energies.append(float(result['energy']))
                    atom = result['atoms']
                    slopes.append([float(atom['slope_right'][native_engine.anchor-1]),float(atom['slope_left'][native_engine.anchor])])
                    curvatures.append([float(atom['second'][native_engine.anchor-1]),float(atom['second'][native_engine.anchor])])
                    radius = nodal_radii(native_engine,data['edges'])
                    fraction = np.asarray([abs((point-data['source'])/((data['edges'][0] if point<data['source'] else data['edges'][-1])-data['source'])) for point in radius],float)
                    core_gradients.append(float(maximum(result['field_gradient'][fraction<.10])))
                    approximate = np.polynomial.chebyshev.chebval(2*label,loads.native_factor_coefficients)
                    interpolation_error = max(interpolation_error,float(np.max(abs(approximate-np.asarray(result['image'],float)))/max(float(maximum(result['image'])),1e-30)))
                    if position==len(points)//2:
                        fast = compensated_shapes(native_engine,data['edges'],data['field'][:,None])[:,0]
                        fast_image_error = float(maximum(fast-result['image'])/max(maximum(result['image']),Decimal('1e-30')))
                    if position%16==15:
                        progress(name+':native label '+str(position+1))
            evidence.check(name+':general_compensated_image',fast_image_error<1e-26,fast_image_error)
            evidence.check(name+':native_factor_interpolation',interpolation_error<2e-8,interpolation_error)
            force = system['force']+native_force
            acceleration = inverse.solve(force.ravel()).reshape(force.shape)
            for repeat in range(2):
                residual = (matrix@acceleration.ravel()).reshape(force.shape)-force
                acceleration -= inverse.solve(residual.ravel()).reshape(force.shape)
            residual = (matrix@acceleration.ravel()).reshape(force.shape)-force
            relative = float(inverse.residual_norm(residual)/inverse.residual_norm(force))
            evidence.check(name+':full_coupled_Euler',relative<2e-11,relative)
            boundary = endpoint_traction(action,material)
            evidence.check(name+':outer_natural_flux',not np.any(boundary))
            radial_nodes = action.solver.nodes
            metric = 1-2*action.solution['state'][0]/radial_nodes
            beta = radial_nodes**2*np.exp(action.solution['state'][1])*np.sqrt(metric)
            radial_energy = float(action.solver.integrated(beta.ravel()*action.solver.fields['gram'][branch])[-1,-1])
            energy = float(weights@np.array(energies))
            energy_error = abs(energy-radial_energy)/max(abs(energy),1e-30)
            evidence.check(name+':native_radial_action_energy',energy_error<2e-8,energy_error)
            if oracle:
                direction = np.zeros_like(acceleration)
                direction[:,:-1] = .01*np.sin(action.knots)[None,:]
                direction[:,-1] = .02
                direct = direct_momentum_jacobian(action,direction,spatial,material,deadline)
                expected = (matrix@direction.ravel()).reshape(direction.shape)
                oracle_error = float(np.max(abs(direct-expected))/max(np.max(abs(expected)),1e-30))
                evidence.check(name+':momentum_Jacobian_oracle',oracle_error<2e-11,oracle_error)
            trace_cardinal,trace_speed,trace_drift = source_geometry(action,points)
            source_acceleration = trace_cardinal@acceleration[:,-1]
            slopes,curvatures = np.array(slopes),np.array(curvatures)
            trace = trace_speed[:,None]*curvatures+(trace_drift+source_acceleration)[:,None]*slopes
            matrix_path = evidence.output/(name+'-mass.npz')
            save_npz(matrix_path,matrix)
            evidence.own(matrix_path,'outputs')
            acceleration_path = save(name+'-acceleration',acceleration=acceleration,force=force,native_force=native_force,
                wave_source_force=system['force'],residual=residual,rates=loads.rates,coordinates=np.asarray(loads.coordinates,str),
                labels=points,weights=weights,slopes=slopes,curvatures=curvatures,trace=trace,source_acceleration=source_acceleration,
                speed_square=trace_speed,drift=trace_drift,native_energy_layers=np.array(energies),core_native_gradient=np.array(core_gradients),boundary_force=boundary)
            record = dict(name=name,branch=branch,spatial=spatial,material=material,acceleration_path=acceleration_path,
                matrix_path=str(matrix_path.relative_to(evidence.root)),Euler_relative=relative,native_energy=energy,
                radial_action_error=energy_error,maximum_trace_residual=float(np.max(abs(trace))),
                maximum_core_native_gradient=max(core_gradients),maximum_acceleration=float(np.max(abs(acceleration))),
                source_acceleration_range=[float(np.min(acceleration[:,-1])),float(np.max(acceleration[:,-1]))])
            evidence.report['results'].append(record)
            evidence.save()
            del system,matrix,inverse
            gc.collect()
            return acceleration,record

        converged = False
        for iteration in range(5):
            progress('core iteration '+str(iteration))
            with localcontext() as context:
                context.prec = 64
                raw = core_basis(base_action.owner,engine,old_loads.coordinates[:,-1],ratios)
                central = raw[:,:,0]@decimals(base_action.cardinal(0.).ravel())
                norm = trial_norm(base_action,central[:,None])[0][0,0]
                amplitude = float(np.sqrt(flat['target_norm']/norm))
                basis = raw*Decimal.from_float(amplitude)
                coordinates = old_loads.coordinates.copy()
                coordinates[:,:-1] = basis[:,:,0].T
            loads,action = live_core(base_action.owner,coordinates,old_loads.rates,packet['mesh'],packet,'primary',deadline)
            radial_residual = float(np.max(abs(action.solver.residual(action.solution['state'],'primary'))))
            evidence.check('iteration'+str(iteration)+':fresh_radial_equations',radial_residual<8e-14,radial_residual)
            state_path = save('iteration'+str(iteration)+'-state',coordinates=np.asarray(coordinates,str),rates=loads.rates,
                edges=action.solver.edges,basis_exact=np.asarray(basis,str),ratios=ratios,amplitude=np.array(amplitude),**action.solution)
            if iteration==0:
                with localcontext() as context:
                    context.prec = 64
                    data = physical_data(engine,loads,action,0.137)
                    trial = np.stack([data['field'],data['field']+Decimal('.001')*decimals(np.maximum(base_action.knots-6,0))],axis=1)
                    movement = movements(engine,data['edges'],data['source'],3)
                    rate = transport(engine,data['edges'],trial,movement)
                    original_image,original_tangent = image_and_tangent(engine,data['edges'],trial,movement,rate)
                    image,tangent,jump,delta_jump = compensated_shapes(engine,data['edges'],trial,movement)
                    scale = max(maximum(image),maximum(tangent),Decimal('1e-30'))
                    error = max(maximum(image-original_image),maximum(tangent-original_tangent))/scale
                    evidence.check('general_hinge_tangent_atom_oracle',error<Decimal('1e-26'),str(error))
                    evidence.check('nonzero_jump_control_present',maximum(jump)>Decimal('1e-5'),str(maximum(jump)))
            acceleration,result = solve_case(loads,action,'primary','iteration'+str(iteration),12,48)
            cardinal,speed_square,drift = source_geometry(action,labels)
            updated = -(drift+cardinal@acceleration[:,-1])/speed_square
            residual = speed_square*ratios+drift+cardinal@acceleration[:,-1]
            change = float(np.max(abs(updated-ratios)))
            item = dict(iteration=iteration,state_path=state_path,ratio_change=change,ratio_equation_residual=float(np.max(abs(residual))),
                amplitude=amplitude,maximum_trace_residual=result['maximum_trace_residual'],radial_residual=radial_residual)
            evidence.report['iterations'].append(item)
            evidence.report.update(primary_state_path=state_path,final_ratios=ratios.tolist(),amplitude=amplitude)
            evidence.save()
            progress('iteration'+str(iteration)+':ratio residual '+str(item['ratio_equation_residual']))
            if item['ratio_equation_residual']<1e-9 and result['maximum_trace_residual']<1e-9:
                converged = True
                break
            ratios = updated
        high_acceleration,high_record = solve_case(loads,action,'primary','primary-16-64',16,64,True)
        source_corner_converged = converged and high_record['maximum_trace_residual']<1e-9
        reference_loads,reference_action = live_core(base_action.owner,coordinates,old_loads.rates,packet['mesh'],packet,'reference',deadline)
        evidence.report['reference_state_path'] = save('reference-state',coordinates=np.asarray(coordinates,str),rates=loads.rates,
            edges=reference_action.solver.edges,**reference_action.solution)
        for spatial,material in [(12,48),(16,64)]:
            solve_case(reference_loads,reference_action,'reference','reference-'+str(spatial)+'-'+str(material),spatial,material,material==64)
        evidence.report.update(seconds=perf_counter()-started,source_corner_iteration_converged=source_corner_converged,
            scope='Nonflat quadratic source core; full coupled curvature iteration, expanded shape solve remains separate.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
