from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from derive_annular_native_shape_stress_20260928 import physical_data, nodal_transport
from annular_native_trial_matrix_20261001 import transport, image_and_tangent
from search_annular_nonzero_shape_constraint_v3_20261001 import profiles, reduced_search
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def pinned_movements(engine, edges, source):
    radius = np.asarray(edges,float)
    fraction = np.where(radius<=float(source),(radius-radius[0])/(float(source)-radius[0]),
        (radius[-1]-radius)/(radius[-1]-float(source)))
    value = profiles(radius)[0]
    boundary = np.where((radius<=float(source))[:,None],value[:1],value[-1:])
    result = value-fraction[:,None]*profiles(float(source))[0]-(1-fraction[:,None])*boundary
    error = float(np.max(abs(result[[0,engine.anchor,-1]])))
    result[[0,engine.anchor,-1]] = 0
    return decimals(result),error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level',choices=['fine','third'],required=True)
    parser.add_argument('--cpu',type=int,choices=[2,4],required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--max-seconds',type=float,default=5400)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-native-shape-state-Jacobian.md')
        evidence.own(evidence.root/'scripts/annular_native_trial_matrix_20261001.py')
        seal_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests = dict(seal['hashes'])
        parent_path = evidence.output.parent/('annular-pinned-shape-constraint-'+args.level+'-attempt01')/'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('pinned_comparator_complete',parent['state']=='complete' and all(row['passed'] for row in parent['checks']))
        for category in ['inputs','outputs']:
            digests.update(parent[category])
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
                return {key:archive[key].copy() for key in archive.files}

        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))

        old = read(str((evidence.output.parent/'annular-native-shape-stress-attempt01/status.json').relative_to(evidence.root)))
        evidence.report.update(level=args.level,rule_outputs=[],searches=[],endpoint_pinned=True,
            source_configuration_held=True,frozen_metric=True,operator='physical_native_kernel',
            centered_weak_P2_transport=True,github_action=False,subagents_used=False)
        for branch in ['reference-reference','MTS-primary']:
            with localcontext() as context:
                context.prec = 64
                loads,action,sources = restore_case(evidence,digests,branch,args.level,deadline)
                packet = read(sources['packet'])
                engine = NativeKernel(action.mesh,packet['gram_support'],branch=='MTS-primary')
                initial = next(item for item in parent['rule_outputs'] if item['branch']==branch)
                search = read(initial['search_path'])
                saved_basis = read(search['basis_path'])
                basis = np.array([Decimal(str(value)) for value in saved_basis['basis_exact'].ravel()],
                    dtype=object).reshape(saved_basis['basis_exact'].shape)
                previous = next(item for item in old['cases'] if item['branch']==branch and item['level']==args.level)
                old_force = read(previous['material_paths'][-1])['average'][3].copy()
                old_force[2] = (3*old_force[2]-old_force[0])/2
                for order in [32,48]:
                    item = next(item for item in parent['rule_outputs'] if item['branch']==branch and item['material']==order)
                    control = read(item['path'])
                    labels,weights = control['labels'],control['weights']
                    forms,potentials = [],[]
                    for position,label in enumerate(labels):
                        data = physical_data(engine,loads,action,label)
                        field = np.einsum('nlb,l->nb',basis,decimals(data['cardinal']))
                        movement,pin_error = pinned_movements(engine,data['edges'],data['source'])
                        field_rate = transport(engine,data['edges'],field,movement)
                        image,tangent = image_and_tangent(engine,data['edges'],field,movement,field_rate)
                        coefficient = np.asarray(engine.apply('sampling',data['beta']),float)
                        native_change = data['beta_radial'][:,None]*movement[engine.native_edges]
                        coefficient_change = engine.sampling@np.asarray(native_change,float)
                        float_image,float_tangent = np.asarray(image,float),np.asarray(tangent,float)
                        work = np.einsum('ai,a,akj->kij',float_image,coefficient,float_tangent)
                        shape = np.einsum('ai,ak,aj->kij',float_image,coefficient_change,float_image)/2
                        current = (work+work.transpose(0,2,1))/2+shape
                        potential = np.einsum('ai,a,aj->ij',float_image,coefficient,float_image)/2
                        forms.append(current)
                        potentials.append(potential)
                        if position==len(labels)//2:
                            evidence.check(branch+':'+str(order)+':endpoint_source_pins',pin_error<2e-14,pin_error)
                            baseline_error = maximum(field[:,0]-data['field'])
                            evidence.check(branch+':'+str(order)+':original_field_retained',baseline_error<Decimal('1e-45'),str(baseline_error))
                            oracle_error = Decimal(0)
                            for column,test in [(0,0),(3,2),(9,12)]:
                                scalar = engine.evaluate(data['edges'],field[:,column],data['beta'])
                                expected_rate = nodal_transport(engine,scalar,movement[:,test])
                                expected_tangent = engine.tangent(data['edges'],field[:,column],movement[:,test],expected_rate)
                                scale = max(maximum(scalar['image']),maximum(expected_tangent),Decimal('1e-40'))
                                error = max(maximum(image[:,column]-scalar['image']),maximum(tangent[:,test,column]-expected_tangent),
                                    maximum(field_rate[:,test,column]-expected_rate))/scale
                                oracle_error = max(oracle_error,error)
                            evidence.check(branch+':'+str(order)+':scalar_native_and_transport_oracle',oracle_error<Decimal('1e-40'),str(oracle_error))
                            candidate = decimals(np.r_[1.,np.linspace(-.03,.04,9)])
                            trial = field@candidate
                            rate = field_rate[:,2,:]@candidate
                            scalar = engine.evaluate(data['edges'],trial,data['beta'])
                            direct = sum(scalar['field_gradient']*rate,Decimal(0))+sum(scalar['edge_gradient']*movement[:,2],Decimal(0))
                            direct += sum(scalar['load']*native_change[:,2],Decimal(0))
                            expected = np.asarray(candidate,float)@current[2]@np.asarray(candidate,float)
                            relative = abs(float(direct)-expected)/(1e-27+1e-11*abs(float(direct)))
                            evidence.check(branch+':'+str(order)+':independent_adjoint_quadratic',relative<=1,relative)
                            perturbations = []
                            for step in [Decimal('1e-8'),Decimal('5e-9')]:
                                energies = []
                                for sign in [-1,1]:
                                    changed = engine.evaluate(data['edges']+sign*step*movement[:,2],
                                        trial+sign*step*rate,data['beta']+sign*step*native_change[:,2],adjoint=False)
                                    energies.append(changed['energy'])
                                numerical = (energies[1]-energies[0])/(2*step)
                                perturbations.append(float(abs(numerical-direct)/max(abs(direct),Decimal('1e-35'))))
                            evidence.check(branch+':'+str(order)+':finite_physical_action_perturbation',max(perturbations)<1e-10,perturbations)
                        if position%8==7 or position==0 or position==len(labels)-1:
                            partial = save(branch+'-partial-'+str(order),labels=labels[:position+1],weights=weights[:position+1],
                                force_layers=np.array(forms),potential_layers=np.array(potentials))
                            evidence.report['progress'] = dict(branch=branch,level=args.level,order=order,label=position+1,
                                seconds=perf_counter()-started,partial=partial)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']),flush=True)
                            if perf_counter()>deadline:
                                raise RuntimeError('Safe label boundary; partial matrices retained')
                    total = np.einsum('l,lkij->kij',weights,np.array(forms))
                    potential = np.einsum('l,lij->ij',weights,np.array(potentials))
                    error = float(np.max(abs(total[:3,0,0]-old_force)))
                    evidence.check(branch+':'+str(order)+':historical_native_force_replay',error<2e-18,error)
                    if branch=='reference-reference':
                        evidence.check(str(order)+':reference_zero',not np.any(total) and not np.any(potential))
                    path = save(branch+'-quadratic-'+str(order),forces=total,norm=control['norm'],potential=potential,
                        force_layers=np.array(forms),norm_layers=control['norm_layers'],potential_layers=np.array(potentials),
                        labels=labels,weights=weights)
                    searches = [reduced_search(total,control['norm'],potential,size) for size in [4,7,10]]
                    for trial in searches:
                        if 'best' in trial:
                            evidence.check(branch+':'+str(order)+':'+str(trial['size'])+':nonzero_norm',trial['best']['norm_relative_error']<2e-8)
                    result = dict(branch=branch,level=args.level,material=order,spatial=item['spatial'],path=path,
                        basis_path=search['basis_path'],basis_coordinate_transform=search['basis_coordinate_transform'],
                        baseline_force=total[:,0,0].tolist(),baseline_field_norm=float(control['norm'][0,0]),
                        searches=searches,physical_equilibrium=False,endpoint_pinned=True,operator='physical_native_kernel')
                    output = evidence.output/(branch+'-search-'+str(order)+'.json')
                    output.write_text(json.dumps(result,indent=2),encoding='utf-8')
                    evidence.own(output,'outputs')
                    evidence.report['rule_outputs'].append(dict(branch=branch,material=order,spatial=item['spatial'],
                        path=path,search_path=str(output.relative_to(evidence.root))))
                    evidence.report['searches'].append(dict(branch=branch,material=order,
                        summaries=[{key:value for key,value in row.items() if key!='attempts'} for row in searches]))
                    evidence.save()
        evidence.report.update(seconds=perf_counter()-started,physical_equilibrium=False,
            fixed_D_search_is_comparator_only=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

