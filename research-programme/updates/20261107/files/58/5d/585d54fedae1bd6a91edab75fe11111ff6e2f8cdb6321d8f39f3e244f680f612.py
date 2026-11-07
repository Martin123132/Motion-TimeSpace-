from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from seal_annular_constrained_state_search_20261001 import independent_sum,bareiss_positive
from search_annular_nonzero_shape_constraint_v3_20261001 import whiten
from analyze_annular_native_shape_state_20261001 import positive_rational
from scipy.sparse import load_npz
from decimal import Decimal,localcontext
from fractions import Fraction
from time import perf_counter
import csv
import ctypes
import json
import numpy as np


def read_archive(path):
    with np.load(path,allow_pickle=False) as archive:
        return {name:archive[name].copy() for name in archive.files}


def rational_separator(forces,norm,size,certificate):
    forces = (forces+forces.transpose(0,2,1))/2
    norm = (norm+norm.T)/2
    coefficients = list(map(Fraction.from_float,certificate['coefficients']))
    coercivity = Fraction.from_float(certificate['coercivity'])
    return [[sum(coefficients[test]*Fraction.from_float(float(forces[test,row,column]))
        for test in range(size-1))-coercivity*Fraction.from_float(float(norm[row,column]))
        for column in range(size)] for row in range(size)]


def validate_acceleration(evidence,result,prefix):
    saved = read_archive(evidence.root/result['acceleration_path'])
    matrix = load_npz(evidence.root/result['matrix_path']).tocsr()
    acceleration,force = saved['acceleration'],saved['force']
    evidence.check(prefix+':finite_arrays',all(np.all(np.isfinite(value)) for value in saved.values() if value.dtype.kind in 'fc'))
    evidence.check(prefix+':dimensions',acceleration.shape==force.shape and matrix.shape==(force.size,force.size))
    evidence.check(prefix+':zero_initial_rates_and_traction',not np.any(saved['rates']) and not np.any(saved['boundary_force']))
    evidence.check(prefix+':complete_force',np.array_equal(force,saved['wave_source_force']+saved['native_force']))
    difference = matrix-matrix.T
    symmetry = float(np.max(abs(difference.data),initial=0)/max(np.max(abs(matrix.data)),1e-30))
    evidence.check(prefix+':Hessian_symmetry',symmetry<2e-12,symmetry)
    residual = matrix@acceleration.ravel()-force.ravel()
    scale = max(float(np.max(abs(force))),1e-30)
    relative = float(np.max(abs(residual))/scale)
    evidence.check(prefix+':Euler_replay',relative<2e-10,relative)
    evidence.check(prefix+':residual_archive',np.max(abs(residual-saved['residual'].ravel()))<2e-13*scale)
    selected = np.unique(np.r_[np.linspace(0,force.size-1,33,dtype=int),
        np.arange(force.shape[0])*force.shape[1]+force.shape[1]-1])
    maximum = Decimal(0)
    with localcontext() as context:
        context.prec = 70
        for row in selected:
            start,stop = matrix.indptr[row:row+2]
            value = sum((Decimal.from_float(float(entry))*Decimal.from_float(float(acceleration.ravel()[column]))
                for entry,column in zip(matrix.data[start:stop],matrix.indices[start:stop])),Decimal(0))
            maximum = max(maximum,abs(value-Decimal.from_float(float(force.ravel()[row]))))
    evidence.check(prefix+':independent_high_precision_rows',float(maximum)/scale<2e-10,dict(rows=len(selected),relative=float(maximum)/scale))
    buffer_maximum = float(np.max(abs(acceleration[:,:-1][:,saved['buffer']])))
    evidence.check(prefix+':buffer_summary_replay',buffer_maximum==result['maximum_buffer_acceleration'] and buffer_maximum<2e-10)
    evidence.check(prefix+':native_buffer_force_zero',not np.any(saved['native_force'][:,:-1][:,saved['buffer']]))
    evidence.check(prefix+':positive_material_rule',np.all(saved['weights']>0) and abs(np.sum(saved['weights'])-1)<2e-13)
    energy = float(saved['weights']@saved['native_energy_layers'])
    evidence.check(prefix+':energy_replay',abs(energy-result['native_energy'])<=1e-30+2e-14*abs(energy))
    if result['branch']=='reference':
        evidence.check(prefix+':empty_operator_control',energy==0 and not np.any(saved['native_force']))
    return saved,relative


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-source-flat-native-analysis-attempt01',__file__)
    started = perf_counter()
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-source-flat-nullspace-separation.md')
        evidence.own(evidence.root/'DERIVATION-20261002-quadratic-source-core-construction.md')
        constructors,searches,states,results,forms = {},{},{},{},{}
        rows,search_rows,certificates = [],[],[]
        for level in ['fine','third']:
            for kind,table,attempt in [('state',constructors,'02'),('search',searches,'01')]:
                relative = 'source-intake/navier-stokes/20260914/annular-source-flat-native-'+kind+'-'+level+'-attempt'+attempt+'/status.json'
                table[level] = verify_report(evidence,relative)
                evidence.check(level+':'+kind+':complete',table[level]['state']=='complete')
            for branch,item in constructors[level]['states'].items():
                states[level,branch] = read_archive(evidence.root/item['path'])
                evidence.check(level+':'+branch+':radial_residual',item['radial_residual']<8e-14,item['radial_residual'])
                evidence.check(level+':'+branch+':untrapped_chart',item['minimum_F']>0,item['minimum_F'])
            evidence.check(level+':matched_initial_data',np.array_equal(states[level,'primary']['coordinates'],states[level,'reference']['coordinates'])
                and np.array_equal(states[level,'primary']['rates'],states[level,'reference']['rates']))
            for item in constructors[level]['results']:
                prefix = level+':'+item['branch']+':'+str(item['material'])
                saved,residual = validate_acceleration(evidence,item,prefix)
                results[level,item['branch'],item['material']] = saved
                rows.append(dict(level=level,branch=item['branch'],material=item['material'],
                    maximum_acceleration=item['maximum_acceleration'],buffer_acceleration=item['maximum_buffer_acceleration'],
                    source_min=item['source_acceleration_range'][0],source_max=item['source_acceleration_range'][1],
                    native_energy=item['native_energy'],native_force=item['maximum_native_force'],Euler_residual=residual,
                    radial_action_relative_error=item['radial_action_relative_error'],valid_for_claim=False))
            for item in searches[level]['rule_outputs']:
                saved = read_archive(evidence.root/item['path'])
                prefix = level+':'+str(item['material'])
                evidence.check(prefix+':finite_forms',all(np.all(np.isfinite(value)) for value in saved.values()))
                with localcontext() as context:
                    context.prec = 75
                    for total,layer in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                        independent_sum(saved['weights'],saved[layer],saved[total])
                        evidence.check(prefix+':'+total+':independent_sum',True)
                forms[level,item['material']] = saved
            for item in searches[level]['searches']:
                size,material = item['size'],item['material']
                saved = forms[level,material]
                best = item['search']['best']
                coefficient = np.array(best['coefficient'])
                predicted = np.einsum('i,kij,j->k',coefficient,saved['forces'][:,:size,:size],coefficient)
                scale = max(float(np.max(abs(predicted))),1e-30)
                evidence.check(level+':'+str(material)+':'+str(size)+':force_replay',
                    np.max(abs(predicted-best['unscaled_forces']))<2e-13*scale)
                norm = float(coefficient@saved['norm'][:size,:size]@coefficient)
                evidence.check(level+':'+str(material)+':'+str(size)+':positive_norm',norm>0 and abs(norm/saved['norm'][0,0]-1)<2e-8)
                record = dict(level=level,material=material,size=size,fitted_root=item['search']['frozen_root'],
                    fitted_max=best['fitted_max'],withheld_max=best['withheld_max'],
                    boundary_hit=best['at_search_boundary'],solver_success=best['solver_success'],
                    nonzero_norm=norm,relative_field_distance=best['relative_field_distance'],
                    certificate_found=bool(item['certificate'] and item['certificate']['found']),valid_for_claim=False)
                common_transform = whiten(saved['norm'])
                common_matrices = np.einsum('ai,kab,bj->kij',common_transform,saved['forces'],common_transform)
                common_scales = np.maximum(np.linalg.norm(common_matrices,axis=(1,2))*saved['norm'][0,0],1e-300)
                record.update(unscaled_force_max=float(np.max(abs(predicted))),
                    common_24mode_scaled_max=float(np.max(abs(predicted)/common_scales)),
                    baseline_common_scaled_max=float(np.max(abs(saved['forces'][:,0,0])/common_scales)),
                    native_potential=best['gram_potential'],baseline_native_potential=float(saved['potential'][0,0]))
                if material==48:
                    low = forms[level,32]
                    transform = whiten(saved['norm'][:size,:size])
                    matrices = np.einsum('ai,kab,bj->kij',transform,saved['forces'][:,:size,:size],transform)
                    scales = np.maximum(np.linalg.norm(matrices,axis=(1,2))*saved['norm'][0,0],1e-300)
                    lower_force = np.einsum('i,kij,j->k',coefficient,low['forces'][:,:size,:size],coefficient)
                    record['lower_rule_max'] = float(np.max(abs(lower_force)/scales))
                    record['live_recompute_candidate'] = bool(item['search']['frozen_root'] and best['withheld_max']<=1e-9 and record['lower_rule_max']<=1e-9)
                    if record['certificate_found']:
                        high_matrix = rational_separator(saved['forces'],saved['norm'],size,item['certificate'])
                        lower_matrix = rational_separator(low['forces'],low['norm'],size,item['certificate'])
                        minors = bareiss_positive(high_matrix)
                        lower_pivots = positive_rational(lower_matrix)
                        certificates.append(dict(level=level,size=size,coercivity=item['certificate']['coercivity'],
                            coefficients=item['certificate']['coefficients'],positive_leading_minors=minors,
                            same_lower_rule_positive=lower_pivots is not None,lower_pivots=lower_pivots))
                        evidence.check(level+':'+str(size)+':independent_exact_certificate',len(minors)==size)
                        record['same_lower_rule_certificate'] = lower_pivots is not None
                search_rows.append(record)
                evidence.report.update(search_summary=search_rows,certificates=certificates)
                evidence.save()
        comparisons = []
        for level in ['fine','third']:
            for branch in ['primary','reference']:
                low,high = results[level,branch,48],results[level,branch,64]
                comparisons.append(dict(level=level,branch=branch,
                    quadrature_acceleration_max_difference=float(np.max(abs(high['acceleration']-low['acceleration']))),
                    quadrature_force_max_difference=float(np.max(abs(high['force']-low['force'])))))
        packets = {level:json.loads((evidence.root/constructors[level]['packet_path']).read_text()) for level in ['fine','third']}
        fine_nodes = list(map(Fraction,packets['fine']['mesh']['nodes']))
        third_lookup = {Fraction(value):index for index,value in enumerate(packets['third']['mesh']['nodes'])}
        restriction = [third_lookup[value] for value in fine_nodes]+[len(third_lookup)]
        refinement = []
        for branch in ['primary','reference']:
            fine,third = results['fine',branch,64],results['third',branch,64]
            difference = third['acceleration'][:,restriction]-fine['acceleration']
            refinement.append(dict(branch=branch,common_node_acceleration_max_difference=float(np.max(abs(difference))),
                source_acceleration_max_difference=float(np.max(abs(difference[:,-1]))),
                fine_buffer_max=float(np.max(abs(fine['acceleration'][:,:-1][:,fine['buffer']]))),
                third_buffer_max=float(np.max(abs(third['acceleration'][:,:-1][:,third['buffer']])))))
        coefficients = list(map(Fraction,[1,0,-4,0,6,0,-4,0,1]))
        for derivative in range(4):
            for endpoint in [-1,1]:
                value = sum((coefficient*Fraction(endpoint)**degree for degree,coefficient in enumerate(coefficients)),Fraction(0))
                evidence.check('exact_bump_jet_'+str(derivative)+'_'+str(endpoint),value==0)
            coefficients = [degree*coefficients[degree] for degree in range(1,len(coefficients))]
        for points in [[Fraction(-4),Fraction(-3),Fraction(-2),Fraction(-1)],
            [Fraction(1),Fraction(2),Fraction(4),Fraction(7)]]:
            value = sum((max(point,Fraction(0))/np.prod([point-other for other in points if other!=point]) for point in points),Fraction(0))
            evidence.check('exact_one_sided_hinge_'+str(points[0]),value==0)
        points = [Fraction(-4,3),Fraction(-2,5),Fraction(3,7),Fraction(9,8)]
        for degree in range(4):
            difference = sum((point**degree/np.prod([point-other for other in points if other!=point]) for point in points),Fraction(0))
            evidence.check('exact_nonuniform_polynomial_control_'+str(degree),difference==int(degree==3))
        count = len(packets['fine']['gram_support'])-3
        diagonal = [Fraction(5,72)]*count
        diagonal[:3] = [Fraction(59097,573104),Fraction(1825,25284),Fraction(491,7056)]
        diagonal[-3:] = diagonal[:3][::-1]
        adjacent = [Fraction(-1,144)]*(count-1)
        adjacent[:2] = [Fraction(253,50568),Fraction(-3,392)]
        adjacent[-2:] = adjacent[:2][::-1]
        margins = diagonal.copy()
        for index,value in enumerate(adjacent):
            margins[index] -= abs(value)
            margins[index+1] -= abs(value)
        for first,last in [(0,2),(count-3,count-1)]:
            margins[first] -= Fraction(1,392)
            margins[last] -= Fraction(1,392)
        evidence.check('exact_template_positive_diagonal_rows',min(margins)>0,str(min(margins)))
        coefficients = list(map(Fraction,[1,0,0,0,-35,84,-70,20]))
        for derivative in range(4):
            for endpoint in [0,1]:
                value = sum((coefficient*Fraction(endpoint)**degree for degree,coefficient in enumerate(coefficients)),Fraction(0))
                evidence.check('exact_core_transition_jet_'+str(derivative)+'_'+str(endpoint),value==int(derivative==0 and endpoint==0))
            coefficients = [degree*coefficients[degree] for degree in range(1,len(coefficients))]
        for name,records in [('coupled-source-flat-comparison',rows),('source-flat-search-comparison',search_rows)]:
            path = evidence.output/(name+'.csv')
            fields = list(dict.fromkeys(key for record in records for key in record))
            with path.open('x',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=fields)
                writer.writeheader()
                writer.writerows(records)
            evidence.own(path,'outputs')
        evidence.report.update(seconds=perf_counter()-started,coupled_summary=rows,search_summary=search_rows,
            quadrature_comparisons=comparisons,refinement=refinement,certificates=certificates,
            live_candidates=[row for row in search_rows if row.get('live_recompute_candidate')],
            source_corner_repaired_in_initial_construction=True,native_constraints_solved=False,
            full_trajectory_computed=False,finite_certificate_not_global_no_go=True,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
