from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive,rational_separator
from seal_annular_constrained_state_search_20261001 import independent_sum,bareiss_positive
from analyze_annular_native_shape_state_20261001 import positive_rational
from search_annular_nonzero_shape_constraint_v3_20261001 import whiten
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_quadratic_core_20261002 import compensated_shapes,source_geometry
from annular_source_flat_native_20261002 import movements,divided_image
from annular_native_trial_matrix_20261001 import transport,image_and_tangent
from annular_physical_native_kernel_20260928 import NativeKernel,decimals,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from probe_annular_Neumann_kernel_family_20261001 import nodal_radii
from scipy.sparse import load_npz
from decimal import Decimal,localcontext
from fractions import Fraction
from time import perf_counter
import ctypes
import csv
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-quadratic-core-analysis-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        base = 'source-intake/navier-stokes/20260914/'
        parent = json.loads((evidence.root/(base+'annular-source-flat-native-integrity-20261002.json')).read_text())
        digests = dict(parent['hashes'])
        constructors,searches,packets,results = {},{},{},{}
        summaries,search_rows,certificates,comparisons = [],[],[],[]
        for level in ['fine','third']:
            constructors[level] = verify_report(evidence,base+'annular-quadratic-core-state-'+level+'-attempt01/status.json')
            searches[level] = verify_report(evidence,base+'annular-quadratic-core-search-'+level+'-attempt01/status.json')
            for report in [constructors[level],searches[level]]:
                evidence.check(level+':authority_complete:'+report['progress']['stage'],report['state']=='complete')
                for category in ['inputs','outputs']:
                    digests.update(report[category])
            construction = constructors[level]
            packets[level] = json.loads((evidence.root/construction['packet_path']).read_text())
            primary = read_archive(evidence.root/construction['primary_state_path'])
            reference = read_archive(evidence.root/construction['reference_state_path'])
            evidence.check(level+':matched_initial_state',np.array_equal(primary['coordinates'],reference['coordinates']) and np.array_equal(primary['rates'],reference['rates']))
            evidence.check(level+':basis_owns_initial_field',np.array_equal(primary['basis_exact'][:,:,0].T,primary['coordinates'][:,:-1]))
            for item in construction['results']:
                prefix = level+':'+item['name']
                saved = read_archive(evidence.root/item['acceleration_path'])
                matrix = load_npz(evidence.root/item['matrix_path']).tocsr()
                acceleration,force = saved['acceleration'],saved['force']
                evidence.check(prefix+':finite_arrays',all(np.all(np.isfinite(value)) for value in saved.values() if value.dtype.kind in 'fc'))
                evidence.check(prefix+':dimensions',acceleration.shape==force.shape and matrix.shape==(force.size,force.size))
                evidence.check(prefix+':force_composition',np.array_equal(force,saved['wave_source_force']+saved['native_force']))
                evidence.check(prefix+':zero_rates_and_natural_flux',not np.any(saved['rates']) and not np.any(saved['boundary_force']))
                symmetry = matrix-matrix.T
                scale = max(float(np.max(abs(force))),1e-30)
                evidence.check(prefix+':symmetric_Hessian',np.max(abs(symmetry.data),initial=0)<2e-12*np.max(abs(matrix.data)))
                residual = matrix@acceleration.ravel()-force.ravel()
                relative = float(np.max(abs(residual))/scale)
                evidence.check(prefix+':Euler_replay',relative<2e-10,relative)
                evidence.check(prefix+':saved_residual',np.max(abs(residual-saved['residual'].ravel()))<2e-13*scale)
                selected = np.unique(np.r_[np.linspace(0,force.size-1,33,dtype=int),np.arange(force.shape[0])*force.shape[1]+force.shape[1]-1])
                maximum_error = Decimal(0)
                with localcontext() as context:
                    context.prec = 70
                    for row in selected:
                        start,stop = matrix.indptr[row:row+2]
                        total = sum((Decimal.from_float(float(value))*Decimal.from_float(float(acceleration.ravel()[column])) for value,column in zip(matrix.data[start:stop],matrix.indices[start:stop])),Decimal(0))
                        maximum_error = max(maximum_error,abs(total-Decimal.from_float(float(force.ravel()[row]))))
                evidence.check(prefix+':independent_Decimal_rows',float(maximum_error)/scale<2e-10,dict(rows=len(selected),relative=float(maximum_error)/scale))
                trace = saved['speed_square'][:,None]*saved['curvatures']+(saved['drift']+saved['source_acceleration'])[:,None]*saved['slopes']
                evidence.check(prefix+':trace_formula',np.array_equal(trace,saved['trace']))
                evidence.check(prefix+':trace_summary',float(np.max(abs(trace)))==item['maximum_trace_residual'])
                evidence.check(prefix+':nonzero_source_slope',np.min(abs(saved['slopes']))>1e-4,float(np.min(abs(saved['slopes']))))
                energy = float(saved['weights']@saved['native_energy_layers'])
                evidence.check(prefix+':energy_summary',abs(energy-item['native_energy'])<1e-30+2e-14*abs(energy))
                if item['branch']=='reference':
                    evidence.check(prefix+':empty_native_control',energy==0 and not np.any(saved['native_force']))
                results[level,item['name']] = saved
                summaries.append(dict(level=level,name=item['name'],branch=item['branch'],material=item['material'],
                    trace_max=item['maximum_trace_residual'],core_native_gradient=item['maximum_core_native_gradient'],
                    source_min=item['source_acceleration_range'][0],source_max=item['source_acceleration_range'][1],
                    native_energy=energy,Euler_replay=relative,valid_for_claim=False))
            with localcontext() as context:
                context.prec = 64
                unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                loads,action = restore_refined(old_action.owner,primary,packets[level]['mesh'],packets[level],'primary',deadline)
                last = construction['iterations'][-1]
                acceleration = results[level,'iteration'+str(last['iteration'])]['acceleration']
                cardinal,speed,drift = source_geometry(action,action.owner.layer_rule.points/2)
                residual = speed*primary['ratios']+drift+cardinal@acceleration[:,-1]
                evidence.check(level+':independent_ratio_equation',np.max(abs(residual))<1e-9,float(np.max(abs(residual))))
                evidence.check(level+':convergence_status',construction['source_corner_iteration_converged'] and np.max(abs(results[level,'primary-16-64']['trace']))<1e-9)
                engine = NativeKernel(action.mesh,packets[level]['gram_support'],True)
                data = physical_data(engine,loads,action,0.137)
                trial = data['field'].copy()
                trial[engine.indices[engine.anchor-1,1]] += Decimal('.003')
                trial[engine.indices[engine.anchor,1]] -= Decimal('.002')
                movement = movements(engine,data['edges'],data['source'],3)
                image,tangent,jump,delta_jump = compensated_shapes(engine,data['edges'],trial[:,None],movement)
                rate = transport(engine,data['edges'],trial[:,None],movement)
                original_image,original_tangent = image_and_tangent(engine,data['edges'],trial[:,None],movement,rate)
                scale = max(maximum(image),maximum(tangent),Decimal('1e-30'))
                difference = max(maximum(image-original_image),maximum(tangent-original_tangent))/scale
                evidence.check(level+':nonzero_delta_jump_oracle',difference<Decimal('1e-26'),str(difference))
                evidence.check(level+':nonzero_delta_jump_excited',maximum(delta_jump)>Decimal('1e-5'),str(maximum(delta_jump)))
                radius = nodal_radii(engine,data['edges'])
                hinge = np.maximum(radius-data['source'],Decimal(0))
                hinge_image = divided_image(engine,data['edges'],hinge)[0]
                omitted = hinge_image[:,None,None]*delta_jump[None,:,:]
                evidence.check(level+':omitting_jump_tangent_detectable',maximum(omitted)/scale>Decimal('1e-5'),str(maximum(omitted)/scale))
            forms = {}
            for item in searches[level]['rule_outputs']:
                saved = read_archive(evidence.root/item['path'])
                forms[item['material']] = saved
                with localcontext() as context:
                    context.prec = 75
                    for total,layer in [('forces','force_layers'),('norm','norm_layers'),('potential','potential_layers')]:
                        independent_sum(saved['weights'],saved[layer],saved[total])
                        evidence.check(level+':'+str(item['material'])+':'+total+':independent_sum',True)
            for item in searches[level]['searches']:
                size,material = item['size'],item['material']
                saved = forms[material]
                best = item['search']['best']
                coefficient = np.array(best['coefficient'])
                force = np.einsum('i,kij,j->k',coefficient,saved['forces'][:,:size,:size],coefficient)
                evidence.check(level+':'+str(material)+':'+str(size)+':force_replay',np.max(abs(force-best['unscaled_forces']))<2e-13*max(np.max(abs(force)),1e-30))
                norm = float(coefficient@saved['norm'][:size,:size]@coefficient)
                evidence.check(level+':'+str(material)+':'+str(size)+':norm',norm>0 and abs(norm/saved['norm'][0,0]-1)<2e-8)
                transform = whiten(saved['norm'])
                matrices = np.einsum('ai,kab,bj->kij',transform,saved['forces'],transform)
                scales = np.maximum(np.linalg.norm(matrices,axis=(1,2))*saved['norm'][0,0],1e-300)
                record = dict(level=level,material=material,size=size,fitted_root=item['search']['frozen_root'],
                    fitted_max=best['fitted_max'],withheld_max=best['withheld_max'],unscaled_force_max=float(np.max(abs(force))),
                    common_26mode_scaled_max=float(np.max(abs(force)/scales)),baseline_common_scaled_max=float(np.max(abs(saved['forces'][:,0,0])/scales)),
                    nonzero_norm=norm,solver_success=best['solver_success'],boundary_hit=best['at_search_boundary'],
                    certificate_found=bool(item['certificate'] and item['certificate']['found']),valid_for_claim=False)
                if material==48:
                    lower_force = np.einsum('i,kij,j->k',coefficient,forms[32]['forces'][:,:size,:size],coefficient)
                    record['lower_rule_common_max'] = float(np.max(abs(lower_force)/scales))
                    record['live_candidate'] = bool(item['search']['frozen_root'] and best['withheld_max']<=1e-9 and record['lower_rule_common_max']<=1e-9)
                    if record['certificate_found']:
                        high_matrix = rational_separator(saved['forces'],saved['norm'],size,item['certificate'])
                        low_matrix = rational_separator(forms[32]['forces'],forms[32]['norm'],size,item['certificate'])
                        minors = bareiss_positive(high_matrix)
                        pivots = positive_rational(low_matrix)
                        certificates.append(dict(level=level,size=size,coefficients=item['certificate']['coefficients'],coercivity=item['certificate']['coercivity'],
                            positive_leading_minors=minors,lower_positive=pivots is not None,lower_pivots=pivots))
                        record['lower_rule_certificate_positive'] = pivots is not None
                        evidence.check(level+':'+str(size)+':exact_certificate_replay',len(minors)==size)
                search_rows.append(record)
            for branch in ['primary','reference']:
                low_name = 'iteration'+str(construction['iterations'][-1]['iteration']) if branch=='primary' else 'reference-12-48'
                low,high = results[level,low_name],results[level,branch+'-16-64']
                comparisons.append(dict(level=level,branch=branch,acceleration_quadrature_difference=float(np.max(abs(high['acceleration']-low['acceleration'])))))
        lookup = {Fraction(value):index for index,value in enumerate(packets['third']['mesh']['nodes'])}
        restriction = [lookup[Fraction(value)] for value in packets['fine']['mesh']['nodes']]+[len(lookup)]
        refinement = []
        for branch in ['primary','reference']:
            fine,third = results['fine',branch+'-16-64'],results['third',branch+'-16-64']
            difference = third['acceleration'][:,restriction]-fine['acceleration']
            refinement.append(dict(branch=branch,acceleration_common_node_difference=float(np.max(abs(difference))),
                source_acceleration_difference=float(np.max(abs(difference[:,-1])))))
        for name,records in [('quadratic-core-coupled-comparison',summaries),('quadratic-core-search-comparison',search_rows)]:
            path = evidence.output/(name+'.csv')
            fields = list(dict.fromkeys(key for row in records for key in row))
            with path.open('x',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=fields)
                writer.writeheader()
                writer.writerows(records)
            evidence.own(path,'outputs')
        evidence.report.update(seconds=perf_counter()-started,coupled_summary=summaries,search_summary=search_rows,
            certificates=certificates,quadrature=comparisons,refinement=refinement,
            live_candidates=[row for row in search_rows if row.get('live_candidate')],
            source_corner_solved_for_baseline=True,joint_source_shape_solved=False,physical_evolution=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
