from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_compensated_acceleration_polynomial_v2_20261001 import decimal_values
from search_annular_nonzero_shape_constraint_v3_20261001 import profiles,reduced_search
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
    parser.add_argument('--label',required=True)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-pinned-constraint-search-correction.md')
        digests = {}
        seal_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        evidence.own(seal_path)
        seal = json.loads(seal_path.read_text())
        digests.update(seal['hashes'])
        parent_path = evidence.output.parent/('annular-nonzero-shape-constraint-'+args.level+'-attempt03')/'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('unconditioned_parent_complete',parent['state']=='complete' and all(row['passed'] for row in parent['checks']))
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
            with np.load(path,allow_pickle=False) as saved:
                return {name:saved[name].copy() for name in saved.files}

        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))

        pinned = read(str((evidence.output.parent/'annular-geometric-pullback-attempt02/status.json').relative_to(evidence.root)))
        evidence.report.update(level=args.level,rule_outputs=[],searches=[],endpoint_pinned=True,
            source_configuration_held=True,frozen_metric=True,github_action=False,subagents_used=False)
        for branch in ['reference-reference','MTS-primary']:
            with localcontext() as context:
                context.prec = 64
                loads,action,sources = restore_case(evidence,digests,branch,args.level,deadline)
                first = next(item for item in parent['rule_outputs'] if item['branch']==branch)
                original_search = read(first['search_path'])
                archived = read(original_search['basis_path'])
                basis = np.array([Decimal(str(value)) for value in archived['basis_exact'].ravel()],dtype=object).reshape(archived['basis_exact'].shape)
                unused,gradient = local_polynomials(action.mesh,basis.reshape(len(action.knots),-1))
                gradient = gradient.reshape(len(action.mesh['elements']),2,len(action.source),10)
                factor_basis = np.asarray(action.factor.apply(basis.reshape(len(action.knots),-1)),float).reshape(action.factor.shape[0],len(action.source),10)
            indices = np.array(action.mesh['elements'])
            counts = np.zeros(len(action.knots))
            np.add.at(counts,indices[indices>=0],1)
            edges = np.array(list(map(float,action.edges)))
            previous = next(row for row in pinned['cases'] if row['branch']==branch and row['level']==args.level)
            old_pinned = read(previous['material_paths'][-1])['average']
            old_force = old_pinned[:,:,:2].sum(axis=2).mean(axis=1)
            old_force[2] = (3*old_force[2]-old_force[0])/2
            for order in [32,48]:
                item = next(row for row in parent['rule_outputs'] if row['branch']==branch and row['material']==order)
                data = read(item['path'])
                search = read(item['search_path'])
                labels,weights = data['labels'],data['weights']
                corrections,forms = [],[]
                for position,label in enumerate(labels):
                    cardinal = np.asarray(action.cardinal(label)).ravel()
                    source = float(cardinal@action.source)
                    geometry = action.geometry(action.knots,source,label)
                    derivative = np.einsum('cplb,l->cpb',gradient,cardinal)
                    node_gradient = np.zeros((len(action.knots),10))
                    for vertex,local in enumerate([0.,.5,1.]):
                        reference = edges[:-1]*(1-local)+edges[1:]*local
                        jacobian = action.mapping(reference,source,label)[1]
                        if local==1:
                            selected = edges[1:]==action.owner.model.anchor
                            jacobian[selected] = (source-action.owner.model.radii[0]-action.owner.width*label)/(action.owner.model.anchor-action.owner.model.radii[0])
                        values = (derivative[:,0]+local*derivative[:,1])/jacobian[:,None]
                        selected = indices[:,vertex]>=0
                        np.add.at(node_gradient,indices[selected,vertex],values[selected])
                    node_gradient /= counts[:,None]
                    left = geometry['radius']<source
                    masks = np.array([left,~left]).T
                    endpoint_eta = (1-geometry['displacement'])[:,None]*masks
                    endpoint_slope = -(geometry['jacobian_source']/geometry['jacobian'])[:,None]*masks
                    with localcontext() as context:
                        context.prec = 64
                        null_values = decimal_values(endpoint_eta)[:,:,None]*decimal_values(node_gradient)[:,None,:]
                        response = np.asarray(action.factor.apply(null_values.reshape(len(action.knots),-1)),float).reshape(action.factor.shape[0],2,10)
                    image = np.einsum('alb,l->ab',factor_basis,cardinal)
                    gamma = geometry['gradient']
                    coefficient = np.asarray(action.sampling@gamma).ravel()
                    strain = 2/geometry['radius']+geometry['lapse_log_radial']+geometry['metric_radial']/(2*geometry['metric'])
                    changed_coefficient = action.sampling@(gamma[:,None]*(strain[:,None]*endpoint_eta-endpoint_slope))
                    work = np.einsum('ai,a,akj->kij',image,coefficient,response)
                    shape = np.einsum('ai,ak,aj->kij',image,changed_coefficient,image)/2
                    endpoint_forms = (work+work.transpose(0,2,1))/2+shape
                    boundary = action.geometry(edges[[0,-1]],source,label)['radius']
                    boundary_profiles = profiles(boundary)[0]
                    correction = np.einsum('sk,sij->kij',boundary_profiles,endpoint_forms)
                    current = data['force_layers'][position]-correction
                    corrections.append(correction)
                    forms.append(current)
                    if position==len(labels)//2:
                        value,slope = profiles(geometry['radius'])
                        source_profile = profiles(source)[0]
                        endpoint_value = np.where(left[:,None],boundary_profiles[0],boundary_profiles[1])
                        eta = value-geometry['displacement'][:,None]*source_profile-(1-geometry['displacement'])[:,None]*endpoint_value
                        slope -= (geometry['jacobian_source']/geometry['jacobian'])[:,None]*(source_profile-endpoint_value)
                        probe = action.geometry(np.array([edges[0],action.owner.model.anchor,edges[-1]]),source,label)
                        endpoint_probe = np.array([boundary_profiles[0],boundary_profiles[1],boundary_profiles[1]])
                        pinned_values = profiles(probe['radius'])[0]-probe['displacement'][:,None]*source_profile
                        pinned_values -= (1-probe['displacement'])[:,None]*endpoint_probe
                        evidence.check(branch+':'+str(order)+':all_13_boundary_source_pins',np.max(abs(pinned_values))<1e-13,float(np.max(abs(pinned_values))))
                        with localcontext() as context:
                            context.prec = 64
                            direct = decimal_values(eta[:,:3])[:,:,None]*decimal_values(node_gradient)[:,None,:]
                            direct_images = np.asarray(action.factor.apply(direct.reshape(len(action.knots),-1)),float).reshape(action.factor.shape[0],3,10)
                        worst = 0.
                        for candidate in [np.eye(10)[0],np.r_[1.,np.linspace(-.03,.04,9)]]:
                            for test in range(3):
                                step = 1e-22
                                moved_radius = geometry['radius']+1j*step*eta[:,test]
                                metric = action.solver.values(action.solution,moved_radius)[0]
                                moved_gamma = moved_radius**2*np.exp(metric[1])*np.sqrt(1-2*metric[0]/moved_radius)/(geometry['jacobian']*(1+1j*step*slope[:,test]))
                                moved_image = image@candidate+1j*step*(direct_images[:,test]@candidate)
                                actual = ((action.sampling@moved_gamma)@moved_image**2/2).imag/step
                                expected = candidate@current[test]@candidate
                                worst = max(worst,float(abs(actual-expected)/(2e-18+2e-8*abs(expected))))
                        evidence.check(branch+':'+str(order)+':direct_pinned_potential_variation',worst<=1,worst)
                    if position%16==15:
                        evidence.report['progress'] = dict(branch=branch,level=args.level,order=order,label=position+1,seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe label boundary')
                total = np.einsum('l,lkij->kij',weights,np.array(forms))
                error = float(np.max(abs(total[:3,0,0]-old_force)))
                evidence.check(branch+':'+str(order)+':historical_pinned_force_replay',error<2e-18,error)
                if branch=='reference-reference':
                    evidence.check(str(order)+':reference_zero',not np.any(total))
                path = save(branch+'-quadratic-'+str(order),forces=total,norm=data['norm'],potential=data['potential'],
                    force_layers=np.array(forms),norm_layers=data['norm_layers'],potential_layers=data['potential_layers'],
                    endpoint_corrections=np.array(corrections),labels=labels,weights=weights)
                searches = [reduced_search(total,data['norm'],data['potential'],size) for size in [4,7,10]]
                for trial in searches:
                    if 'best' in trial:
                        evidence.check(branch+':'+str(order)+':'+str(trial['size'])+':nonzero_norm',trial['best']['norm_relative_error']<2e-8)
                result = dict(branch=branch,level=args.level,material=order,spatial=item['spatial'],path=path,
                    basis_path=search['basis_path'],basis_coordinate_transform=search['basis_coordinate_transform'],
                    baseline_force=total[:,0,0].tolist(),baseline_field_norm=float(data['norm'][0,0]),
                    searches=searches,physical_equilibrium=False,endpoint_pinned=True)
                output = evidence.output/(branch+'-search-'+str(order)+'.json')
                output.write_text(json.dumps(result,indent=2),encoding='utf-8')
                evidence.own(output,'outputs')
                evidence.report['rule_outputs'].append(dict(branch=branch,material=order,spatial=item['spatial'],path=path,search_path=str(output.relative_to(evidence.root))))
                evidence.report['searches'].append(dict(branch=branch,material=order,summaries=[{key:value for key,value in row.items() if key!='attempts'} for row in searches]))
                evidence.save()
        evidence.report.update(seconds=perf_counter()-started,unpinned_certificates_superseded=True,physical_equilibrium=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

