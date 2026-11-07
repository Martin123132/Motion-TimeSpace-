from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_source_flat_native_20261002 import flat_basis,live_native_flat,trial_norm,divided_image
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from annular_zero_rate_euler_20261001 import zero_rate_system,endpoint_traction,direct_momentum_jacobian
from annular_native_source_hinge_20261002 import source_hinge_image
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
    evidence = EvidenceRun('annular-source-flat-native-state-'+args.level+'-attempt02',__file__)
    started,deadline = perf_counter(),perf_counter()+7200
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-source-flat-native-compatible-initial-data.md')
        evidence.own(evidence.root/'DERIVATION-20261002-exact-source-hinge-support.md')
        parent_path = evidence.output.parent/'annular-null-coupled-acceleration-integrity-20261001.json'
        evidence.own(parent_path)
        parent = json.loads(parent_path.read_text())
        digests = parent['hashes']
        evidence.check('complete_parent',parent['state']=='complete' and not parent['mismatches'])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe stage boundary; completed files retained')
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        progress('restore parent')
        with localcontext() as context:
            context.prec = 64
            previous_loads,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            packet_path = evidence.root/sources['packet']
            packet = json.loads(packet_path.read_text())
            evidence.own(packet_path)
            raw = flat_basis(old_action.knots,old_action.owner.model.anchor,float(old_action.edges[0]),float(old_action.edges[-1]))
            old_norm = trial_norm(old_action,np.asarray(previous_loads.coordinates[:,:-1],float).T@old_action.cardinal(0.).ravel()[:,None])[0][0,0]
            norm = trial_norm(old_action,raw[:,:1])[0][0,0]
            amplitude = float(np.sqrt(old_norm/norm))
            field = decimals(amplitude*raw[:,0])
            coordinates = previous_loads.coordinates.copy()
            coordinates[:,:-1] = field[None,:]
            rates = np.zeros_like(previous_loads.rates)
        evidence.check('nonzero_old_norm',old_norm>0 and amplitude>0)
        evidence.check('source_configuration_retained',np.array_equal(coordinates[:,-1],previous_loads.coordinates[:,-1]))
        evidence.report.update(level=args.level,packet_path=str(packet_path.relative_to(evidence.root)),sources=sources,
            amplitude=amplitude,target_norm=float(old_norm),results=[],states={},physical_trajectory_computed=False,
            native_constraints_solved=False,github_action=False,subagents_used=False)
        for branch in ['primary','reference']:
            progress(branch+':fresh native radial geometry')
            loads,action = live_native_flat(old_action.owner,coordinates,rates,packet['mesh'],packet,branch,deadline)
            engine = NativeKernel(action.mesh,packet['gram_support'],branch=='primary')
            residual = float(np.max(np.abs(action.solver.residual(action.solution['state'],branch))))
            evidence.check(branch+':native_radial_residual',residual<8e-14,residual)
            radius = action.solver.nodes
            metric = 1-2*action.solution['state'][0]/radius
            beta = radius**2*np.exp(action.solution['state'][1])*np.sqrt(metric)
            radial_energy = float(action.solver.integrated((beta.ravel()*action.solver.fields['gram'][branch]))[-1,-1])
            state_path = save(branch+'-initial-data',coordinates=np.asarray(coordinates,str),rates=rates,
                edges=action.solver.edges,native_gram_density=action.solver.fields['gram'][branch],radial_nodes=radius,**action.solution)
            evidence.report['states'][branch] = dict(path=state_path,radial_residual=residual,
                radial_energy=radial_energy,minimum_F=float(np.min(metric)))
            for spatial,material in [(12,48),(16,64)]:
                prefix = branch+'-'+str(spatial)+'-'+str(material)
                progress(prefix+':coupled Hessian')
                system = zero_rate_system(action,spatial,material,deadline,lambda stage:progress(prefix+':'+stage))
                matrix,inverse = system['matrix'],system['inverse']
                force = system['force'].copy()
                native_force = np.zeros_like(force)
                points,weights = np.polynomial.legendre.leggauss(material)
                points,weights = points/2,weights/2
                weights *= 6*(points+.5)*(.5-points)
                energies,maximum_buffer_gradient,maximum_hinge_overlap = [],0.,0.
                factor_interpolation_error = 0.
                with localcontext() as context:
                    context.prec = 64
                    for position,(label,weight) in enumerate(zip(points,weights)):
                        data = physical_data(engine,loads,action,label)
                        result = engine.evaluate(data['edges'],data['field'],data['beta'])
                        source_gradient = sum(result['edge_gradient']*data['displacement'],Decimal(0))
                        source_gradient += sum(result['load']*data['beta_radial']*data['displacement'][engine.native_edges],Decimal(0))
                        covector = np.r_[np.asarray(result['field_gradient'],float),float(source_gradient)]
                        native_force -= weight*np.outer(data['cardinal'],covector)
                        energies.append(float(result['energy']))
                        nodes = nodal_radii(engine,data['edges'])
                        fraction = np.asarray([abs((point-data['source'])/((data['edges'][0] if point<data['source'] else data['edges'][-1])-data['source'])) for point in nodes],float)
                        buffer = (fraction<.10)|(fraction>.90)
                        maximum_buffer_gradient = max(maximum_buffer_gradient,float(maximum(result['field_gradient'][buffer])))
                        hinge = np.array([max(point-data['source'],Decimal(0)) for point in nodes],dtype=object)
                        hinge_image = source_hinge_image(engine,data['edges'],data['source'])
                        if position==len(points)//2:
                            numerical_hinge = divided_image(engine,data['edges'],hinge)[0]
                            evidence.check(prefix+':affine_hinge_support_identity',maximum(hinge_image-numerical_hinge)<Decimal('1e-35'))
                        maximum_hinge_overlap = max(maximum_hinge_overlap,float(maximum(hinge_image*result['image'])))
                        approximate = np.polynomial.chebyshev.chebval(2*label,loads.native_factor_coefficients)
                        factor_interpolation_error = max(factor_interpolation_error,
                            float(np.max(np.abs(approximate-np.asarray(result['image'],float)))/max(float(maximum(result['image'])),1e-30)))
                        if position%16==15:
                            progress(prefix+':native force label '+str(position+1))
                evidence.check(prefix+':no_hidden_native_source_boundary_force',maximum_buffer_gradient==0,maximum_buffer_gradient)
                evidence.check(prefix+':hinge_support_disjoint_rowwise',maximum_hinge_overlap==0,maximum_hinge_overlap)
                evidence.check(prefix+':native_factor_material_interpolation',factor_interpolation_error<2e-8,factor_interpolation_error)
                direct_energy = float(weights@np.array(energies))
                energy_relative = abs(direct_energy-radial_energy)/max(abs(direct_energy),1e-30)
                evidence.check(prefix+':native_radial_action_energy',energy_relative<2e-8,energy_relative)
                force += native_force
                acceleration = inverse.solve(force.ravel()).reshape(force.shape)
                for repeat in range(2):
                    defect = (matrix@acceleration.ravel()).reshape(force.shape)-force
                    acceleration -= inverse.solve(defect.ravel()).reshape(force.shape)
                defect = (matrix@acceleration.ravel()).reshape(force.shape)-force
                relative = inverse.residual_norm(defect)/inverse.residual_norm(force)
                evidence.check(prefix+':full_native_coupled_Euler',relative<2e-11,float(relative))
                boundary = endpoint_traction(action,material)
                evidence.check(prefix+':wave_endpoint_traction_zero',not np.any(boundary))
                reference_fraction = np.abs((action.knots-action.owner.model.anchor)/
                    np.where(action.knots<action.owner.model.anchor,float(action.edges[0])-action.owner.model.anchor,float(action.edges[-1])-action.owner.model.anchor))
                buffer = (reference_fraction<.10)|(reference_fraction>.90)
                field_buffer = float(np.max(np.abs(acceleration[:,:-1][:,buffer])))
                evidence.check(prefix+':source_boundary_acceleration_small',field_buffer<2e-10,field_buffer)
                direction = np.zeros_like(acceleration)
                direction[:,:-1] = .01*np.sin(action.knots)[None,:]
                direction[:,-1] = .02
                direct = direct_momentum_jacobian(action,direction,spatial,material,deadline)
                expected = (matrix@direction.ravel()).reshape(direction.shape)
                oracle = float(np.max(np.abs(direct-expected))/max(np.max(np.abs(expected)),1e-30))
                evidence.check(prefix+':independent_momentum_Jacobian',oracle<2e-11,oracle)
                matrix_path = evidence.output/(prefix+'-mass.npz')
                save_npz(matrix_path,matrix)
                evidence.own(matrix_path,'outputs')
                acceleration_path = save(prefix+'-acceleration',acceleration=acceleration,force=force,
                    wave_source_force=system['force'],native_force=native_force,residual=defect,
                    rates=rates,coordinates=np.asarray(coordinates,str),buffer=buffer,labels=points,weights=weights,
                    native_energy_layers=np.array(energies),boundary_force=boundary)
                summary = dict(branch=branch,spatial=spatial,material=material,acceleration_path=acceleration_path,
                    matrix_path=str(matrix_path.relative_to(evidence.root)),maximum_acceleration=float(np.max(np.abs(acceleration))),
                    source_acceleration_range=[float(np.min(acceleration[:,-1])),float(np.max(acceleration[:,-1]))],
                    maximum_buffer_acceleration=field_buffer,native_energy=direct_energy,
                    maximum_native_force=float(np.max(np.abs(native_force))),Euler_relative=float(relative),
                    momentum_oracle_relative=oracle,radial_action_relative_error=energy_relative)
                evidence.report['results'].append(summary)
                evidence.save()
                del system,matrix,inverse
                gc.collect()
        evidence.report.update(seconds=perf_counter()-started,source_corner_fixed_without_acceleration_fit=True,
            native_Gram_force_retained=True,source_acceleration_fitted=False,
            scope='New source-flat nonzero initial state with full native and matched reference coupling; shape constraint search is separate.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

