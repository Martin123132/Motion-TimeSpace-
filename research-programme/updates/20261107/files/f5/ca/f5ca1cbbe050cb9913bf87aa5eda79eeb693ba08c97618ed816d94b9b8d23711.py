from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_compensated_acceleration_polynomial_v2_20261001 import decimal_values
from decimal import localcontext
from scipy.optimize import least_squares
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np


def profiles(radius,count=13):
    coordinate = (np.asarray(radius)-6)/.9
    envelope = np.maximum(1-coordinate**2,0)
    polynomials = np.polynomial.legendre.legvander(coordinate,count-1)
    values = polynomials*envelope[...,None]**4
    derivatives = []
    for degree in range(count):
        coefficients = np.zeros(degree+1)
        coefficients[-1] = 1
        slope = np.polynomial.legendre.legval(coordinate,np.polynomial.legendre.legder(coefficients))
        derivatives.append((-8*coordinate*envelope**3*polynomials[...,degree]+envelope**4*slope)/.9)
    return values,np.stack(derivatives,axis=-1)


def whiten(gram):
    columns = []
    for index in range(len(gram)):
        vector = np.eye(len(gram))[:,index]
        for repeat in range(2):
            for column in columns:
                vector -= column*(column@gram@vector)
        norm = float(vector@gram@vector)
        if norm<=1e-20*gram[0,0]:
            return None
        columns.append(vector/np.sqrt(norm))
    return np.array(columns).T


def reduced_search(forces,gram,potential,size):
    gram = gram[:size,:size]
    transform = whiten(gram)
    if transform is None:
        return dict(size=size,state='unresolved_trial_rank',frozen_root=False)
    transformed = np.einsum('ai,kab,bj->kij',transform,forces[:,:size,:size],transform)
    scale = np.maximum(np.linalg.norm(transformed,axis=(1,2)),1e-300)
    conditioned = transformed/scale[:,None,None]
    fitted = size-1

    def evaluate(theta,all_tests=False):
        vector = np.r_[1.,theta]
        norm = vector@vector
        selected = conditioned if all_tests else conditioned[:fitted]
        product = np.einsum('kij,j->ki',selected,vector)
        quadratic = product@vector
        residual = quadratic/norm
        jacobian = 2*(product[:,1:]*norm-quadratic[:,None]*vector[1:])/norm**2
        return residual,jacobian

    test = np.linspace(-.13,.17,size-1)
    residual,jacobian = evaluate(test)
    complex_jacobian = np.column_stack([evaluate(test.astype(complex)+1e-23j*np.eye(size-1)[index])[0].imag/1e-23
        for index in range(size-1)])
    oracle = float(np.max(abs(jacobian-complex_jacobian)))
    if oracle>2e-12:
        raise RuntimeError('Normalized analytic Jacobian failed')
    starts = [np.zeros(size-1)]
    for direction in range(min(3,size-1)):
        for sign in [-1,1]:
            point = np.zeros(size-1)
            point[direction] = sign*.5
            starts.append(point)
    attempts = []
    for start in starts:
        result = least_squares(lambda theta:evaluate(theta)[0],start,jac=lambda theta:evaluate(theta)[1],
            bounds=(-20,20),ftol=1e-13,xtol=1e-13,gtol=1e-13,max_nfev=350)
        residual,jacobian = evaluate(result.x)
        all_residual,unused = evaluate(result.x,True)
        vector = np.r_[1.,result.x]
        coefficient = np.sqrt(gram[0,0])*(transform@vector)/np.linalg.norm(vector)
        norm = coefficient@gram@coefficient
        distance = np.sqrt(max(0.,2-2/np.linalg.norm(vector)))
        attempts.append(dict(theta=result.x.tolist(),coefficient=coefficient.tolist(),nfev=result.nfev,
            solver_success=bool(result.success),status=int(result.status),message=result.message,
            fitted_max=float(np.max(abs(residual))),withheld_max=float(np.max(abs(all_residual[fitted:]))),
            all_scaled_residuals=all_residual.tolist(),fixed_norm=float(norm),
            norm_relative_error=float(abs(norm/gram[0,0]-1)),relative_field_distance=float(distance),
            singular_values=np.linalg.svd(jacobian,compute_uv=False).tolist(),
            at_search_boundary=bool(np.any(abs(result.x)>19.999)),
            unscaled_forces=np.einsum('i,kij,j->k',coefficient,forces[:,:size,:size],coefficient).tolist(),
            gram_potential=float(coefficient@potential[:size,:size]@coefficient)))
    accepted = [item for item in attempts if item['fitted_max']<=1e-9 and not item['at_search_boundary']]
    best = min(accepted,key=lambda item:item['relative_field_distance']) if accepted else min(attempts,key=lambda item:item['fitted_max'])
    return dict(size=size,state='frozen_moment_root' if accepted else 'no_root_found_in_search',
        frozen_root=bool(accepted),fitted_tests=fitted,withheld_tests=len(forces)-fitted,
        normalization='fixed_nonzero_background_L2_not_conserved_energy',jacobian_oracle_error=oracle,
        whitening_error=float(np.max(abs(transform.T@gram@transform-np.eye(size)))),
        baseline_forces=forces[:,0,0].tolist(),attempts=attempts,best=best,
        metric_recomputed=False,physical_equilibrium=False)


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
        raise OSError('CPU affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+5400
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-nonzero-shape-constraint-state-search.md')
        seal_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('complete_parent',seal['state']=='complete' and not seal['mismatches'])
        digests = {}
        for relative,expected in seal['hashes'].items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed parent '+relative)
            digests[str(path.relative_to(evidence.root))] = expected

        def save(name,**arrays):
            path = evidence.output/(name+'.npz')
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            return str(path.relative_to(evidence.root))

        old_path = evidence.output.parent/'annular-support-map-constraints-attempt01/status.json'
        evidence.own(old_path)
        old = json.loads(old_path.read_text())
        evidence.report.update(level=args.level,rule_outputs=[],searches=[],frozen_metric=True,
            fixed_source_configuration=True,github_action=False,subagents_used=False,new_trajectories=0)
        for branch in ['reference-reference','MTS-primary']:
            with localcontext() as context:
                context.prec = 64
                loads,action,sources = restore_case(evidence,digests,branch,args.level,deadline)
                fields = decimal_values(loads.coordinates[:,:-1].T)
                basis = np.empty(fields.shape+(10,),dtype=object)
                basis[:,:,0] = fields
                for label_index,label in enumerate(action.owner.layer_rule.points/2):
                    radius = action.mapping(action.knots,action.source[label_index],label)[0]
                    multiplier = profiles(radius,9)[0]
                    basis[:,label_index,1:] = fields[:,label_index,None]*decimal_values(multiplier)
                packed = basis.reshape(len(action.knots),-1)
                polynomial,gradient = local_polynomials(action.mesh,packed)
                gradient = gradient.reshape(len(action.mesh['elements']),2,fields.shape[1],10)
                factor_basis = np.asarray(action.factor.apply(packed),float).reshape(action.factor.shape[0],fields.shape[1],10)
            evidence.check(branch+':base_factor_replay',np.array_equal(factor_basis[:,:,0],action.factor_values))
            basis_path = save(branch+'-field-basis',basis=np.asarray(basis,float),
                basis_exact=np.asarray(basis,str),source=action.source,rates=loads.rates)
            indices = np.array(action.mesh['elements'])
            valid = indices>=0
            counts = np.zeros(len(action.knots))
            np.add.at(counts,indices[valid],1)
            for spatial,material in [(8,32),(12,48)]:
                labels,weights = np.polynomial.legendre.leggauss(material)
                labels,weights = labels/2,weights/2
                weights *= 6*(labels+.5)*(.5-labels)
                all_forces,all_norms,all_potentials = [],[],[]
                for label_index,label in enumerate(labels):
                    cardinal = np.asarray(action.cardinal(label)).ravel()
                    source = float(cardinal@action.source)
                    source_profile = profiles(source)[0]
                    node_geometry = action.geometry(action.knots,source,label)
                    value,slope = profiles(node_geometry['radius'])
                    eta = value-node_geometry['displacement'][:,None]*source_profile
                    eta_slope = slope-(node_geometry['jacobian_source']/node_geometry['jacobian'])[:,None]*source_profile
                    derivative = np.einsum('cplb,l->cpb',gradient,cardinal)
                    node_gradient = np.zeros((len(action.knots),10))
                    edges = np.array(list(map(float,action.edges)))
                    for vertex,local in enumerate([0.,.5,1.]):
                        reference = edges[:-1]*(1-local)+edges[1:]*local
                        jacobian = action.mapping(reference,source,label)[1]
                        if local==1:
                            at_anchor = edges[1:]==action.owner.model.anchor
                            jacobian[at_anchor] = (source-action.owner.model.radii[0]-action.owner.width*label)/(action.owner.model.anchor-action.owner.model.radii[0])
                        values = (derivative[:,0]+local*derivative[:,1])/jacobian[:,None]
                        selected = indices[:,vertex]>=0
                        np.add.at(node_gradient,indices[selected,vertex],values[selected])
                    node_gradient /= counts[:,None]
                    with localcontext() as context:
                        context.prec = 64
                        null_values = decimal_values(eta)[:,:,None]*decimal_values(node_gradient)[:,None,:]
                        null_images = np.asarray(action.factor.apply(null_values.reshape(len(action.knots),-1)),float)
                        null_images = null_images.reshape(action.factor.shape[0],13,10)
                    image = np.einsum('alb,l->ab',factor_basis,cardinal)
                    gamma = node_geometry['gradient']
                    coefficient = np.asarray(action.sampling@gamma).ravel()
                    strain = 2/node_geometry['radius']+node_geometry['lapse_log_radial']+node_geometry['metric_radial']/(2*node_geometry['metric'])
                    shape_coefficient = action.sampling@(gamma[:,None]*(strain[:,None]*eta-eta_slope))
                    work = np.einsum('ai,a,akj->kij',image,coefficient,null_images)
                    shape = np.einsum('ai,ak,aj->kij',image,shape_coefficient,image)/2
                    forms = (work+work.transpose(0,2,1))/2+shape
                    potential = (image.T*coefficient)@image/2
                    quadrature = action.quadrature(label,source,spatial)
                    cells,local = quadrature['cells'],quadrature['local']
                    local_basis = np.array([(1-local)*(1-2*local),4*local*(1-local),local*(2*local-1)]).T
                    actual_indices = indices[cells]
                    local_basis *= actual_indices>=0
                    nodal = np.einsum('nlb,l->nb',np.asarray(basis,float),cardinal)
                    field = np.einsum('qv,qvb->qb',local_basis,nodal[np.maximum(actual_indices,0)])
                    geometry = action.geometry(quadrature['reference'],source,label)
                    norm = (field.T*(quadrature['measure']*geometry['kinetic']))@field
                    all_forces.append(forms)
                    all_norms.append(norm)
                    all_potentials.append(potential)
                    if label_index==material//2:
                        candidates = [np.eye(10)[0],np.r_[1.,np.linspace(-.03,.04,9)]]
                        worst = 0.
                        for candidate in candidates:
                            for test in range(3):
                                for step in [1e-18,1e-22]:
                                    moved_radius = node_geometry['radius']+1j*step*eta[:,test]
                                    moved_jacobian = node_geometry['jacobian']*(1+1j*step*eta_slope[:,test])
                                    metric_values = action.solver.values(action.solution,moved_radius)[0]
                                    moved_gamma = moved_radius**2*np.exp(metric_values[1])*np.sqrt(1-2*metric_values[0]/moved_radius)/moved_jacobian
                                    moved_image = image@candidate+1j*step*(null_images[:,test]@candidate)
                                    varied = ((action.sampling@moved_gamma)@moved_image**2/2).imag/step
                                    expected = candidate@forms[test]@candidate
                                    error = abs(varied-expected)/(2e-18+2e-8*abs(expected))
                                    worst = max(worst,float(error))
                        evidence.check(branch+':'+str(material)+':independent_potential_variation',worst<=1,worst)
                    if label_index%8==7:
                        temporary = evidence.output/(branch+'-'+str(material)+'-partial.npz')
                        with temporary.open('wb') as stream:
                            np.savez_compressed(stream,forces=np.array(all_forces),norms=np.array(all_norms),
                                potentials=np.array(all_potentials),labels=labels,weights=weights,next_label=label_index+1)
                        evidence.report['progress'] = dict(branch=branch,level=args.level,material=material,label=label_index+1,
                            seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']),flush=True)
                        if perf_counter()>deadline:
                            raise RuntimeError('Safe completed material-label boundary')
                forms = np.einsum('l,lkij->kij',weights,np.array(all_forces))
                norm = np.einsum('l,lij->ij',weights,np.array(all_norms))
                potential = np.einsum('l,lij->ij',weights,np.array(all_potentials))
                path = save(branch+'-quadratic-'+str(material),forces=forms,norm=norm,potential=potential,
                    force_layers=np.array(all_forces),norm_layers=np.array(all_norms),
                    potential_layers=np.array(all_potentials),labels=labels,weights=weights)
                case = next(item for item in old['cases'] if item['branch']==branch and item['level']==args.level)
                expected = np.array(case['shape_work'])
                expected[2] = (3*expected[2]-expected[0])/2
                replay = float(np.max(abs(forms[:3,0,0]-expected)))
                evidence.check(branch+':'+str(material)+':baseline_shape_force_replay',replay<2e-18,replay)
                evidence.check(branch+':'+str(material)+':positive_nonzero_field_norm',norm[0,0]>0,float(norm[0,0]))
                if branch=='reference-reference':
                    evidence.check(str(material)+':reference_force_exact_zero',not np.any(forms))
                searches = [reduced_search(forms,norm,potential,size) for size in [4,7,10]]
                for search in searches:
                    if 'best' in search:
                        evidence.check(branch+':'+str(material)+':size'+str(search['size'])+':nonzero_norm',
                            search['best']['norm_relative_error']<2e-8,search['best']['norm_relative_error'])
                result = dict(branch=branch,level=args.level,material=material,spatial=spatial,path=path,
                    basis_path=basis_path,baseline_force=forms[:,0,0].tolist(),baseline_field_norm=float(norm[0,0]),
                    searches=searches,physical_equilibrium=False)
                json_path = evidence.output/(branch+'-search-'+str(material)+'.json')
                json_path.write_text(json.dumps(result,indent=2),encoding='utf-8')
                evidence.own(json_path,'outputs')
                evidence.report['rule_outputs'].append(dict(branch=branch,material=material,spatial=spatial,path=path,
                    search_path=str(json_path.relative_to(evidence.root))))
                evidence.report['searches'].append(dict(branch=branch,material=material,
                    summaries=[{key:value for key,value in item.items() if key not in ['attempts']} for item in searches]))
                evidence.save()
        evidence.report.update(seconds=perf_counter()-started,full_metric_recomputed_for_new_state=False,
            nonlinear_constraint_search_performed=True,physical_equilibrium=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()

