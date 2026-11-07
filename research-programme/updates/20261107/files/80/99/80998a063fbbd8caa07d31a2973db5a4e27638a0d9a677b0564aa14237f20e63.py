from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_candidate_midpoint_20260921 import CommonCoordinateAction
from annular_source_flat_native_20261002 import live_native_flat,movements,shape_forms
from annular_native_source_hinge_20261002 import source_hinge_image
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from derive_annular_native_shape_stress_20260928 import physical_data,nodal_transport
from search_annular_nonzero_shape_constraint_v3_20261001 import whiten
from decimal import Decimal,localcontext
from time import perf_counter
import argparse
import ctypes
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
    evidence = EvidenceRun('annular-source-flat-live-feedback-'+args.level+'-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+5400
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-source-flat-live-feedback.md')
        parent_path = evidence.output.parent/'annular-null-coupled-acceleration-integrity-20261001.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        reports = {}
        for kind,attempt in [('state','02'),('search','01')]:
            path = evidence.output.parent/('annular-source-flat-native-'+kind+'-'+args.level+'-attempt'+attempt)/'status.json'
            evidence.own(path)
            report = json.loads(path.read_text())
            evidence.check(kind+':complete',report['state']=='complete' and all(row['passed'] for row in report['checks']))
            for category in ['inputs','outputs']:
                digests.update(report[category])
            reports[kind] = report
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed source '+relative)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Safe stage boundary; completed outputs retained')
        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))
        selected = next(row for row in reports['search']['searches'] if row['material']==48 and row['size']==24)
        coefficient = np.array(selected['search']['best']['coefficient'])
        with np.load(evidence.root/reports['search']['basis_path'],allow_pickle=False) as archive:
            basis = np.array([Decimal(str(value)) for value in archive['basis_exact'].ravel()],dtype=object).reshape(archive['basis_exact'].shape)
        with np.load(evidence.root/reports['state']['states']['primary']['path'],allow_pickle=False) as archive:
            state = {name:archive[name].copy() for name in archive.files}
        packet = json.loads((evidence.root/reports['state']['packet_path']).read_text())
        with localcontext() as context:
            context.prec = 64
            unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',args.level,deadline)
            old_loads,base_action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
            coordinates = old_loads.coordinates.copy()
            coordinates[:,:-1] = (basis@decimals(coefficient))[None,:]
        evidence.check('source_and_rates_retained',np.array_equal(coordinates[:,-1],old_loads.coordinates[:,-1]) and not np.any(old_loads.rates))
        evidence.report.update(level=args.level,selected_size=24,source_acceleration_fitted=False,
            candidate_selection='Largest predeclared family, best fitted result; withheld tests do not select it.',
            frozen_root=selected['search']['frozen_root'],exploratory_nonroot_probe=not selected['search']['frozen_root'],results=[])
        progress('fresh native metric on selected trial')
        loads,action = live_native_flat(old_action.owner,coordinates,old_loads.rates,packet['mesh'],packet,'primary',deadline)
        solver,solution = action.solver,action.solution
        old_values = base_action.solver.values(base_action.solution,solver.nodes.ravel())[0].reshape(solution['state'].shape)
        old_residual = float(np.max(abs(solver.residual(old_values,'primary'))))
        new_residual = float(np.max(abs(solver.residual(solution['state'],'primary'))))
        metric = 1-2*solution['state'][0]/solver.nodes
        evidence.check('fresh_native_radial_equations',new_residual<8e-14,new_residual)
        evidence.check('untrapped_metric',float(np.min(metric))>0,float(np.min(metric)))
        beta = solver.nodes**2*np.exp(solution['state'][1])*np.sqrt(metric)
        radial_energy = float(solver.integrated(beta.ravel()*solver.fields['gram']['primary'])[-1,-1])
        metric_path = save('fresh-native-metric',edges=solver.edges,centers=solver.centers,lengths=solver.lengths,
            coordinates=np.asarray(coordinates,str),rates=loads.rates,coefficient=coefficient,**solution)
        frozen = CommonCoordinateAction(action.owner,coordinates,loads.rates,packet['mesh'],loads,base_action.solver,base_action.solution,64)
        engine = NativeKernel(action.mesh,packet['gram_support'],True)
        for name,current,order in [('frozen_replay',frozen,48),('live_low',action,32),('live_high',action,48)]:
            progress(name)
            labels,weights = np.polynomial.legendre.leggauss(order)
            labels,weights = labels/2,weights/2
            weights *= 6*(labels+.5)*(.5-labels)
            layers,energies = [],[]
            with localcontext() as context:
                context.prec = 64
                for position,label in enumerate(labels):
                    data = physical_data(engine,loads,current,label)
                    movement = movements(engine,data['edges'],data['source'])
                    force,potential,image,unused,unused2 = shape_forms(engine,data,data['field'][:,None],movement)
                    layers.append(force[:,0,0])
                    energies.append(float(potential[0,0]))
                    if position==len(labels)//2:
                        scalar = engine.evaluate(data['edges'],data['field'],data['beta'])
                        test = 11
                        field_rate = nodal_transport(engine,scalar,movement[:,test])
                        direct = sum(scalar['field_gradient']*field_rate,Decimal(0))+sum(scalar['edge_gradient']*movement[:,test],Decimal(0))
                        direct += sum(scalar['load']*data['beta_radial']*movement[engine.native_edges,test],Decimal(0))
                        error = abs(float(direct)-float(force[test,0,0]))/max(abs(float(direct)),1e-30)
                        evidence.check(name+':independent_scalar_adjoint',error<2e-10,error)
                        evidence.check(name+':source_hinge_support_disjoint',maximum(source_hinge_image(engine,data['edges'],data['source'])*image[:,0])==0)
                    if position%16==15:
                        progress(name+':label '+str(position+1))
            layers,energies = np.array(layers),np.array(energies)
            total,energy = weights@layers,float(weights@energies)
            path = save(name,labels=labels,weights=weights,layers=layers,total=total,energy_layers=energies,energy=np.array(energy))
            evidence.report['results'].append(dict(name=name,path=path,force=total.tolist(),native_energy=energy))
            evidence.save()
        predicted = np.array(selected['search']['best']['unscaled_forces'])
        replay,low,high = [np.array(row['force']) for row in evidence.report['results']]
        replay_relative = float(np.max(abs(replay-predicted))/max(np.max(abs(predicted)),1e-30))
        evidence.check('frozen_quadratic_force_replay',replay_relative<2e-9,replay_relative)
        direct_energy = evidence.report['results'][-1]['native_energy']
        energy_relative = abs(direct_energy-radial_energy)/max(abs(direct_energy),1e-30)
        evidence.check('live_native_radial_action_energy',energy_relative<2e-8,energy_relative)
        form_path = next(row['path'] for row in reports['search']['rule_outputs'] if row['material']==48)
        with np.load(evidence.root/form_path,allow_pickle=False) as archive:
            transform = whiten(archive['norm'])
            matrices = np.einsum('ai,kab,bj->kij',transform,archive['forces'],transform)
            scales = np.maximum(np.linalg.norm(matrices,axis=(1,2))*archive['norm'][0,0],1e-300)
        evidence.report.update(seconds=perf_counter()-started,metric_path=metric_path,
            old_metric_residual_on_new_field=old_residual,fresh_metric_residual=new_residual,
            maximum_mass_change=float(np.max(abs(solution['state'][0]-old_values[0]))),
            maximum_log_lapse_change=float(np.max(abs(solution['state'][1]-old_values[1]))),
            native_radial_action_relative_error=energy_relative,
            frozen_force_max=float(np.max(abs(replay))),live_force_max=float(np.max(abs(high))),
            live_force_change_max=float(np.max(abs(high-replay))),quadrature_force_change_max=float(np.max(abs(high-low))),
            frozen_common_scaled_max=float(np.max(abs(replay)/scales)),live_common_scaled_max=float(np.max(abs(high)/scales)),
            lower_rule_common_scaled_max=float(np.max(abs(low)/scales)),native_constraints_solved=False,
            full_trajectory_computed=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
