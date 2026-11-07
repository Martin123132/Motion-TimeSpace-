from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import live_refined
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_native_trial_matrix_20261001 import transport, image_and_tangent
from search_annular_native_shape_state_20261001 import pinned_movements
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import ctypes
import hashlib
import json
import numpy as np
import sympy as sp


def nodal_radii(engine,edges):
    result = np.full(engine.count,Decimal(0),dtype=object)
    for local,values in [(0,edges[:-1]),(1,(edges[:-1]+edges[1:])/2),(2,edges[1:])]:
        selected = engine.indices[:,local]>=0
        result[engine.indices[selected,local]] = values[selected]
    return result


def unit_profile(radius,lower,source,upper):
    return np.array([(point-(lower if point<=source else upper))**2-(source-(lower if point<=source else upper))**2 for point in radius],dtype=object)


def central_norm(action,nodal,source):
    quadrature = action.quadrature(0.,source,12)
    local = quadrature['local']
    shape = np.array([(1-local)*(1-2*local),4*local*(1-local),local*(2*local-1)]).T
    indices = np.array(action.mesh['elements'])[quadrature['cells']]
    shape *= indices>=0
    field = np.sum(shape*np.asarray(nodal,float)[np.maximum(indices,0)],axis=1)
    geometry = action.geometry(quadrature['reference'],source,0.)
    return float(np.sum(quadrature['measure']*geometry['kinetic']*field**2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpu',type=int,default=2)
    parser.add_argument('--label',default='annular-Neumann-kernel-family-attempt01')
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+5400
    try:
        evidence.own(evidence.root/'DERIVATION-20261001-nonzero-kernel-family-and-preservation.md')
        evidence.own(evidence.root/'DERIVATION-20261001-kernel-native-radial-reconciliation.md')
        evidence.own(evidence.root/'DERIVATION-20261001-Neumann-kernel-initial-slice.md')
        evidence.own(evidence.root/'DERIVATION-20261001-null-family-source-corner-compatibility.md')
        for script in ['annular_native_trial_matrix_20261001.py','search_annular_native_shape_state_20261001.py']:
            evidence.own(evidence.root/'scripts'/script)
        seal_path = evidence.output.parent/'annular-common-jet-jump-stage-integrity-20261001.json'
        evidence.own(seal_path)
        parent = json.loads(seal_path.read_text())
        digests = dict(parent['hashes'])
        for relative,expected in digests.items():
            path = (evidence.root/relative).resolve()
            if not path.is_relative_to(evidence.root) or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise RuntimeError('Changed source '+relative)
        radius,lower,source,upper,amplitude = sp.symbols('R L b U a',positive=True)
        left = amplitude*((radius-lower)**2-(source-lower)**2)
        right = amplitude*((radius-upper)**2-(source-upper)**2)
        jump = 2*amplitude*(lower-upper)
        evidence.check('symbolic_compensated_common_quadratic',sp.expand(right-jump*(radius-source)-left)==0)
        evidence.check('symbolic_Neumann_and_source_pins',sp.diff(left,radius).subs(radius,lower)==0 and left.subs(radius,source)==0
            and right.subs(radius,source)==0 and sp.diff(right,radius).subs(radius,upper)==0)
        evidence.check('symbolic_equal_curvature',sp.diff(left,radius,2)==sp.diff(right,radius,2)==2*amplitude)
        speed_square_symbol,drift_symbol = sp.symbols('c2 d',positive=True)
        required_left = -drift_symbol-2*amplitude*speed_square_symbol/sp.diff(left,radius).subs(radius,source)
        required_right = -drift_symbol-2*amplitude*speed_square_symbol/sp.diff(right,radius).subs(radius,source)
        gap = speed_square_symbol*(1/(source-lower)+1/(upper-source))
        evidence.check('two_sided_source_acceleration_gap',sp.simplify(required_right-required_left-gap)==0)
        for side,field in [('left',left),('right',right)]:
            endpoint = lower if side=='left' else upper
            wave = sp.diff(field,radius,2)+2*sp.diff(field,radius)/radius
            evidence.check(side+':flat_acceleration',sp.simplify(wave-amplitude*(6-4*endpoint/radius))==0)
            evidence.check(side+':nonquadratic_preservation_obstruction',
                sp.simplify(sp.diff(wave,radius,3)-24*amplitude*endpoint/radius**4)==0)
        evidence.check('outer_higher_Neumann_compatibility_mismatch',
            sp.simplify(sp.diff(sp.diff(right,radius,2)+2*sp.diff(right,radius)/radius,radius).subs(radius,upper)-4*amplitude/upper)==0)
        evidence.report.update(scope='Nonzero instantaneous native-Gram kernel initial data and explicit preservation tests',
            action_coefficients_unchanged=True,original_trajectory_unchanged=True,source_profile_changed=True,first_Neumann_boundary_satisfied=True,
            rates_reset_to_zero=True,github_action=False,subagents_used=False)
        for level in ['fine','third']:
            evidence.report['progress'] = dict(level=level,stage='restore',seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            with localcontext() as context:
                context.prec = 64
                loads,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                packet_path = evidence.root/sources['packet']
                evidence.own(packet_path)
                packet = json.loads(packet_path.read_text())
                engine = NativeKernel(old_action.mesh,packet['gram_support'],True)
                old = physical_data(engine,loads,old_action,0.)
                nodes = nodal_radii(engine,old['edges'])
                unit = unit_profile(nodes,old['edges'][0],old['source'],old['edges'][-1])
                old_norm = central_norm(old_action,old['field'],float(old['source']))
                unit_norm = central_norm(old_action,unit,float(old['source']))
                amplitude_value = Decimal.from_float(float(np.sqrt(old_norm/unit_norm)))
                field = amplitude_value*unit
                coordinates = np.empty(loads.coordinates.shape,dtype=object)
                coordinates[:,:-1] = field[None,:]
                coordinates[:,-1] = old['source']+Decimal.from_float(float(old_action.owner.width))*decimals(old_action.owner.layer_rule.points/2)
                rates = np.zeros_like(loads.rates)
                evidence.check(level+':nonzero_norm',old_norm>0 and abs(central_norm(old_action,field,float(old['source']))/old_norm-1)<1e-12,old_norm)
                evidence.report['progress'] = dict(level=level,stage='fresh radial metric for constructed state',seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']),flush=True)
                new_loads,action = live_refined(old_action.owner,coordinates,rates,packet['mesh'],packet,'primary',deadline)
                residual = float(np.max(abs(action.solver.residual(action.solution['state'],'primary'))))
                evidence.check(level+':fresh_radial_constraints',residual<8e-14,residual)
                metric = 1-2*action.solution['state'][0]/action.solver.nodes
                clock_square = np.exp(2*action.solution['state'][1])
                old_gram = action.solver.fields['gram']['primary']
                radial_nodes = action.solver.nodes.ravel()
                original_rhs = action.solver.rhs(action.solution['state'],'primary')
                correction = np.array([action.owner.coupling*radial_nodes**2*metric.ravel()*old_gram,
                    action.owner.coupling*radial_nodes*old_gram])
                native_rhs = original_rhs-correction
                mass_integral,lapse_integral = [action.solver.integrated(values) for values in native_rhs]
                outer_value = .5*np.log(1-2*action.solution['state'][0,-1,-1]/action.solver.edges[-1])
                native_residual_array = np.array([action.solution['state'][0]-action.owner.central_mass-mass_integral,
                    action.solution['state'][1]-outer_value-lapse_integral+lapse_integral[-1,-1]])
                native_residual = float(np.max(abs(native_residual_array)))
                evidence.check(level+':actual_native_null_radial_constraints',native_residual<8e-14,native_residual)
                evidence.check(level+':discarded_fixed_reference_load_is_numerically_negligible',np.max(abs(old_gram))<1e-30,float(np.max(abs(old_gram))))
                rhs_path = evidence.output/(level+'-native-radial-residual.npz')
                np.savez_compressed(rhs_path,radius=radial_nodes,old_gram=old_gram,old_rhs=original_rhs,
                    native_rhs=native_rhs,correction=correction,residual=native_residual_array,
                    state=action.solution['state'],kappa=np.array(action.owner.coupling))
                evidence.own(rhs_path,'outputs')
                evidence.check(level+':untrapped_timelike',np.min(metric)>0 and np.min(clock_square)>0)
                path = evidence.output/(level+'-constructed-initial-data.npz')
                np.savez_compressed(path,coordinates=np.asarray(coordinates,str),rates=rates,
                    amplitude=np.array(str(amplitude_value)),edges=action.solver.edges,**action.solution)
                evidence.own(path,'outputs')
                rows = []
                corner_rows = []
                for label in [-.45,0.,.37]:
                    data = physical_data(engine,new_loads,action,label)
                    analytic = amplitude_value*unit_profile(nodal_radii(engine,data['edges']),
                        data['edges'][0],data['source'],data['edges'][-1])
                    ideal = engine.evaluate(data['edges'],analytic,data['beta'])
                    actual = engine.evaluate(data['edges'],data['field'],data['beta'])
                    evidence.check(level+':'+str(label)+':analytic_kernel_zero',maximum(ideal['image'])<Decimal('1e-40'),str(maximum(ideal['image'])))
                    movement,pin_error = pinned_movements(engine,data['edges'],data['source'])
                    transported = transport(engine,data['edges'],data['field'][:,None],movement)
                    image,tangent = image_and_tangent(engine,data['edges'],data['field'][:,None],movement,transported)
                    coefficient_change = engine.sampling@np.asarray(data['beta_radial'][:,None]*movement[engine.native_edges],float)
                    force = np.einsum('a,a,ak->k',np.asarray(image[:,0],float),np.asarray(actual['weights'],float),np.asarray(tangent[:,:,0],float))
                    force += np.sum(np.asarray(image[:,0],float)[:,None]**2*coefficient_change/2,axis=0)
                    evidence.check(level+':'+str(label)+':rounded_native_leakage',maximum(actual['image'])<Decimal('1e-18')
                        and max(abs(force))<1e-20,dict(image=str(maximum(actual['image'])),shape_force=float(max(abs(force)))))
                    reference = NativeKernel(action.mesh,packet['gram_support'],False).evaluate(data['edges'],data['field'],data['beta'],adjoint=False)
                    evidence.check(level+':'+str(label)+':matched_empty_operator_control',reference['energy']==0 and maximum(reference['image'])==0)
                    rows.append(dict(label=label,analytic_image_max=str(maximum(ideal['image'])),
                        represented_image_max=str(maximum(actual['image'])),represented_energy=str(actual['energy']),
                        maximum_shape_force=float(max(abs(force))),analytic_vs_represented_field=str(maximum(analytic-data['field']))))
                    source_radius = float(data['source'])
                    source_values,source_derivatives = action.solver.values(action.solution,np.array([source_radius]))
                    source_metric = 1-2*source_values[0,0]/source_radius
                    source_metric_radial = -2*source_derivatives[0,0]/source_radius+2*source_values[0,0]/source_radius**2
                    source_speed_square = np.exp(2*source_values[1,0])*source_metric
                    drift = source_speed_square*(2/source_radius+source_derivatives[1,0]+source_metric_radial/(2*source_metric))
                    left_required = -drift-source_speed_square/(source_radius-float(data['edges'][0]))
                    right_required = -drift+source_speed_square/(float(data['edges'][-1])-source_radius)
                    spreads = []
                    for offset in [1e-6,1e-7,1e-8,1e-10,1e-12]:
                        points = np.array([source_radius-offset,source_radius+offset])
                        values,derivatives = action.solver.values(action.solution,points)
                        metric_values = 1-2*values[0]/points
                        metric_slopes = -2*derivatives[0]/points+2*values[0]/points**2
                        drift_values = np.exp(2*values[1])*metric_values*(2/points+derivatives[1]+metric_slopes/(2*metric_values))
                        spreads.append(dict(offset=offset,drift_jump=float(drift_values[1]-drift_values[0])))
                    corner_rows.append(dict(label=label,required_left=float(left_required),required_right=float(right_required),
                        acceleration_gap=float(right_required-left_required),drift=float(drift),speed_square=float(source_speed_square),
                        observed_drift_spreads=spreads))
                    evidence.check(level+':'+str(label)+':source_corner_gap_resolved',right_required-left_required>0
                        and abs(spreads[-1]['drift_jump'])<1e-5*(right_required-left_required))
                central = physical_data(engine,new_loads,action,0.)
                acceleration_rows = []
                fit_reports = []
                for side in ['left','right']:
                    low,high = (float(central['edges'][0]),float(central['source'])) if side=='left' else (float(central['source']),float(central['edges'][-1]))
                    points = np.linspace(low+.05*(high-low),high-.05*(high-low),101)
                    values,derivative = action.solver.values(action.solution,points)
                    metric = 1-2*values[0]/points
                    metric_radial = -2*derivative[0]/points+2*values[0]/points**2
                    speed_square = np.exp(2*values[1])*metric
                    speed_product = speed_square*(derivative[1]+metric_radial/(2*metric))
                    endpoint = float(central['edges'][0 if side=='left' else -1])
                    gradient = 2*float(amplitude_value)*(points-endpoint)
                    acceleration = 2*float(amplitude_value)*speed_square+(2*speed_square/points+speed_product)*gradient
                    coordinate = 2*(points-low)/(high-low)-1
                    design = np.polynomial.legendre.legvander(coordinate,2)
                    coefficients = np.linalg.lstsq(design,acceleration,rcond=None)[0]
                    remainder = acceleration-design@coefficients
                    report = dict(side=side,max_acceleration=float(max(abs(acceleration))),
                        max_nonquadratic_remainder=float(max(abs(remainder))),
                        relative_L2_remainder=float(np.linalg.norm(remainder)/np.linalg.norm(acceleration)),
                        degree2_projection_coefficients=coefficients.tolist())
                    fit_reports.append(report)
                    acceleration_rows.append(np.array([points,acceleration,remainder]).T)
                diagnostic = evidence.output/(level+'-interior-preservation.npz')
                np.savez_compressed(diagnostic,left=acceleration_rows[0],right=acceleration_rows[1])
                evidence.own(diagnostic,'outputs')
                result = dict(level=level,amplitude=str(amplitude_value),norm=old_norm,
                    maximum_source_profile_change=float(np.max(abs(np.asarray(coordinates[:,-1],float)-old_action.source))),
                    maximum_removed_field_rate=float(np.max(abs(loads.rates[:,:-1]))),
                    maximum_removed_source_rate=float(np.max(abs(loads.rates[:,-1]))),
                    fresh_metric_residual=residual,native_metric_residual=native_residual,old_gram_density_max=float(np.max(abs(old_gram))),native_rhs_path=str(rhs_path.relative_to(evidence.root)),native_probes=rows,interior_preservation=fit_reports,source_corner=corner_rows,
                    initial_data_path=str(path.relative_to(evidence.root)),diagnostic_path=str(diagnostic.relative_to(evidence.root)),
                    instantaneous_analytic_Gram_constraint=True,dynamic_preservation_established=False,
                    flat_control_family_invariant=False,full_source_acceleration_solved=False)
                evidence.report['cases'].append(result)
                evidence.save()
        evidence.report.update(seconds=perf_counter()-started,full_equilibrium_solved=False,
            result='Constructed nonzero native-Gram-null initial slice satisfying the parent natural endpoint flux condition; higher time preservation remains to be tested.')
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
