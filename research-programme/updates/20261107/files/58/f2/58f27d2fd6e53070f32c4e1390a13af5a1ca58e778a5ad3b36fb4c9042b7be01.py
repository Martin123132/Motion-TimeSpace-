from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import restore_refined
from annular_physical_native_kernel_20260928 import NativeKernel,maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from construct_annular_live_transmission_20261002 import two_parabolas
from scipy.sparse import load_npz
from decimal import Decimal,localcontext
from fractions import Fraction
from time import perf_counter
import ctypes
import csv
import json
import numpy as np
import sympy as sp


def independent_energy(action,radius,values,left,right,order=16):
    split = np.unique(np.r_[radius,action.solver.edges])
    split = split[(split>=radius[0])&(split<=radius[-1])]
    nodes,weights = np.polynomial.legendre.leggauss(order)
    probes = ((split[:-1]+split[1:])[:,None]+np.diff(split)[:,None]*nodes[None,:])/2
    measure = np.diff(split)[:,None]*weights[None,:]/2
    probes = probes.ravel()
    cell = np.clip(np.searchsorted(radius,probes,side='right')-1,0,len(radius)-2)
    width = radius[cell+1]-radius[cell]
    coordinate = (probes-radius[cell])/width
    delta = values[cell+1]-values[cell]
    linear = width*right[cell]
    quadratic = 3*delta-width*(2*right[cell]+left[cell+1])
    cubic = -2*delta+width*(right[cell]+left[cell+1])
    field = values[cell]+coordinate*(linear+coordinate*(quadratic+coordinate*cubic))
    gradient = (linear+coordinate*(2*quadratic+3*coordinate*cubic))/width
    metric_values,unused = action.solver.values(action.solution,probes)
    speed = np.exp(metric_values[1])*np.sqrt(1-2*metric_values[0]/probes)
    return float(measure.ravel()@(probes**2*speed*gradient**2/2)),float(measure.ravel()@(probes**2/speed*field**2))


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p,ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<4):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-native-transmission-analysis-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+3600
    try:
        evidence.own(evidence.root/'DERIVATION-20261002-source-geodesic-reduction-under-transmission.md')
        base = 'source-intake/navier-stokes/20260914/'
        names = ['annular-native-interface-transmission-attempt01','annular-native-transmission-material-attempt01',
            'annular-native-carrier-denominator-repair-attempt02','annular-live-native-transmission-third-attempt02']
        reports = {name:verify_report(evidence,base+name+'/status.json') for name in names}
        evidence.check('all_input_runs_complete',all(report['state']=='complete' for report in reports.values()))
        probe,survey,carrier,live = [reports[name] for name in names]
        parent_path = evidence.output.parent/'annular-source-flat-native-integrity-20261002.json'
        evidence.own(parent_path)
        digests = dict(json.loads(parent_path.read_text())['hashes'])
        for report in reports.values():
            for category in ['inputs','outputs']:
                digests.update(report[category])
        failed = json.loads((evidence.root/(base+'annular-native-carrier-denominator-repair-attempt01/status.json')).read_text())
        evidence.own(evidence.root/(base+'annular-native-carrier-denominator-repair-attempt01/status.json'))
        evidence.check('retained_carrier_summary_failure_only',failed['state']=='failed' and "bad operand type for abs(): 'list'" in failed['error'] and all(row['passed'] for row in failed['checks']))
        old = read_archive(evidence.root/(base+'annular-native-carrier-denominator-repair-attempt01/fine-carrier-survey.npz'))
        new = read_archive(evidence.root/carrier['cases'][0]['path'])
        evidence.check('failed_attempt_saved_data_identical_to_daughter',old.keys()==new.keys() and all(np.array_equal(old[name],new[name]) for name in old))
        mass,metric,lapse,velocity,lapse_radial,radius,metric_radial,slope,curvature = sp.symbols('M F N v Nr R Fr p k',positive=True)
        lagrangian = -mass*sp.sqrt(lapse**2-velocity**2/metric)
        inertia = sp.diff(lagrangian,velocity,2).subs(velocity,0)
        force = (sp.diff(lagrangian,lapse)*lapse_radial).subs(velocity,0)
        evidence.check('proper_clock_inertia_derived',sp.simplify(inertia-mass/(metric*lapse))==0)
        evidence.check('zero_rate_source_geodesic_derived',sp.simplify(force/inertia+metric*lapse*lapse_radial)==0)
        speed = lapse**2*metric
        drift = speed*(2/radius+lapse_radial/lapse+metric_radial/(2*metric))
        trace = speed*curvature+(drift+force/inertia)*slope
        evidence.check('lapse_cancels_source_curvature_law',sp.simplify(trace-speed*(curvature+(2/radius+metric_radial/(2*metric))*slope))==0)
        beta,minus,plus = sp.symbols('beta gminus gplus',real=True)
        endpoint = beta*(minus**2-plus**2)/2-beta*minus**2+beta*plus**2
        evidence.check('moving_fixed_trace_pressure_sign',sp.simplify(endpoint-beta*(plus**2-minus**2)/2)==0)
        width = Fraction(7,5)
        values = np.array([Fraction(2,7),Fraction(-3,11)],dtype=object)
        outgoing,incoming = Fraction(5,13),Fraction(-7,17)
        midpoint = 2*(values[1]-values[0])/width-(outgoing+incoming)/2
        half_value = values[0]+width*(outgoing+midpoint)/4
        evidence.check('two_parabola_midpoint_value_exact',half_value==values[1]-width*(incoming+midpoint)/4)
        actual = two_parabolas(np.array([Fraction(0),width/2,width],dtype=object),np.array([Fraction(0),width],dtype=object),values,
            np.array([outgoing,incoming],dtype=object),np.array([outgoing,incoming],dtype=object))
        evidence.check('two_parabola_implementation_exact',np.array_equal(actual,np.array([values[0],half_value,values[1]],dtype=object)))
        evidence.check('two_parabola_endpoint_jets_exact',outgoing+2*(midpoint-outgoing)*Fraction(0)==outgoing and incoming-2*(incoming-midpoint)*Fraction(0)==incoming)
        evidence.check('two_parabola_midpoint_C1_exact',outgoing+2*(midpoint-outgoing)/2==incoming-2*(incoming-midpoint)/2)
        summary,live_rows,geodesic = [],[],[]
        with localcontext() as context:
            context.prec = 75
            for level in ['fine','third']:
                construction = verify_report(evidence,base+'annular-quadratic-core-state-'+level+'-attempt01/status.json')
                for category in ['inputs','outputs']:
                    digests.update(construction[category])
                state = read_archive(evidence.root/construction['primary_state_path'])
                packet = json.loads((evidence.root/construction['packet_path']).read_text())
                unused,old_action,sources = restore_case(evidence,digests,'MTS-primary',level,deadline)
                loads,action = restore_refined(old_action.owner,state,packet['mesh'],packet,'primary',deadline)
                engine = NativeKernel(action.mesh,packet['gram_support'],True)
                original_case = next(row for row in probe['cases'] if row['level']==level)
                original = read_archive(evidence.root/original_case['path'])
                original_A = np.array([Decimal(value) for value in original['field_load_exact']],dtype=object)
                original_C = np.array([Decimal(value) for value in original['shape_load_exact']],dtype=object)
                original_mean = np.array([Decimal(value) for value in original['mean_target_exact']],dtype=object)
                evidence.check(level+':original_point_balance_replay',maximum(original_A*original_mean+original_C)<Decimal('1e-24'))
                survey_case = next(row for row in survey['cases'] if row['level']==level)
                sampled = read_archive(evidence.root/survey_case['path'])
                brackets = np.argwhere((sampled['field_load'][:-1]*sampled['field_load'][1:]<0)&sampled['active'][None,:])
                evidence.check(level+':denominator_brackets_replay',np.array_equal(brackets,sampled['brackets']) and len(brackets)==survey_case['sign_change_brackets'])
                for root in survey_case['localized_roots']:
                    data = physical_data(engine,loads,action,root['last_label'])
                    result = engine.evaluate(data['edges'],data['field'],data['beta'])
                    indices = np.r_[engine.indices[:,0],engine.indices[-1,2]][engine.native_edges]
                    knot = root['knot']
                    field = result['field_gradient'][indices[knot]]
                    shape = result['edge_gradient'][engine.native_edges[knot]]+result['load'][knot]*data['beta_radial'][knot]
                    error = max(abs(field-Decimal(root['A'])),abs(shape-Decimal(root['C'])))
                    evidence.check(level+':root_full_atom_oracle:'+str(root['last_label']),error<Decimal('1e-30'),str(error))
                    evidence.check(level+':root_ill_conditioned_mean:'+str(root['last_label']),abs(Decimal(root['C']))>1000000*abs(Decimal(root['A'])))
                case = next(row for row in carrier['cases'] if row['level']==level)
                saved = read_archive(evidence.root/case['path'])
                exact = read_archive(evidence.root/case['exact_path'])
                decoded = {name:np.array([Decimal(value) for value in exact[name]],dtype=object) for name in exact if name!='active'}
                active = exact['active']
                epsilon = Decimal(case['epsilon'])
                evidence.check(level+':carrier_values_replay',maximum(decoded['values']-decoded['original_values']-epsilon*decoded['carrier_values'])<Decimal('1e-50'))
                evidence.check(level+':carrier_force_linearity_replay',maximum(decoded['A']-decoded['original_A']-epsilon*decoded['carrier_A'])<Decimal('1e-35'))
                evidence.check(level+':carrier_slope_jump_replay',maximum(decoded['beta']*(decoded['right']-decoded['left'])-decoded['A'])<Decimal('1e-35'))
                evidence.check(level+':carrier_pressure_replay',maximum(decoded['beta']*(decoded['right']**2-decoded['left']**2)/2+decoded['C'])<Decimal('1e-35'))
                dominance = maximum(decoded['original_A'][active]/(epsilon*decoded['carrier_A'][active]))
                evidence.check(level+':carrier_central_dominance',dominance<Decimal('.501'),str(dominance))
                evidence.check(level+':withheld_dominance_summary',float(np.max(saved['dominance_ratio']))==case['max_sampled_dominance_ratio'] and np.max(saved['dominance_ratio'])<1)
                evidence.check(level+':nonzero_sampled_A',np.all(saved['field_load'][:,saved['active']]!=0))
                float_point = saved['field_load']*saved['target_mean']+saved['shape_load']
                float_jump = saved['beta']*(saved['right']-saved['left'])-saved['field_load']
                evidence.check(level+':all_sampled_point_replay',np.max(abs(float_point))<2e-20,float(np.max(abs(float_point))))
                evidence.check(level+':all_sampled_jump_replay',np.max(abs(float_jump))<2e-15,float(np.max(abs(float_jump))))
                energy_error,norm_error = 0.,0.
                for index,label in enumerate(saved['labels']):
                    energy,norm = independent_energy(action,saved['radius'][index],saved['native_values'][index],saved['left'][index],saved['right'][index])
                    energy_error = max(energy_error,abs(energy/saved['wave_energy'][index]-1))
                    norm_error = max(norm_error,abs(norm/saved['positive_norm'][index]-1))
                evidence.check(level+':all_sampled_energy_independent',energy_error<2e-8,energy_error)
                evidence.check(level+':all_sampled_norm_independent',norm_error<2e-8,norm_error)
                summary.append(dict(level=level,labels=len(saved['labels']),epsilon=str(epsilon),dominance_max=case['max_sampled_dominance_ratio'],
                    maximum_gradient=case['maximum_target_gradient'],central_energy_ratio=case['central_wave_energy_ratio'],
                    old_denominator_brackets=len(brackets),energy_replay_error=energy_error,norm_replay_error=norm_error,valid_for_claim=False))
                if level=='third':
                    live_base_action = old_action
                    live_packet = packet
        coordinates_reference = None
        with localcontext() as context:
            context.prec = 70
            for item in live['results']:
                prefix = 'live:'+item['name']
                saved = read_archive(evidence.root/item['path'])
                matrix = load_npz(evidence.root/item['matrix_path']).tocsr()
                evidence.check(prefix+':force_composition',np.array_equal(saved['force'],saved['native_force']+saved['wave_source_force']))
                evidence.check(prefix+':zero_rates_and_flux',not np.any(saved['rates']) and not np.any(saved['boundary_force']))
                defect = matrix-matrix.T
                evidence.check(prefix+':symmetric_mass',np.max(abs(defect.data),initial=0)<2e-12*np.max(abs(matrix.data)))
                residual = matrix@saved['acceleration'].ravel()-saved['force'].ravel()
                scale = max(float(np.max(abs(saved['force']))),1e-30)
                relative = float(np.max(abs(residual))/scale)
                evidence.check(prefix+':coupled_equation_replay',relative<2e-10,relative)
                error = Decimal(0)
                for row_index in np.unique(np.r_[np.linspace(0,matrix.shape[0]-1,33,dtype=int),np.arange(saved['force'].shape[0])*saved['force'].shape[1]+saved['force'].shape[1]-1]):
                    first,last = matrix.indptr[row_index:row_index+2]
                    value = sum((Decimal.from_float(float(coefficient))*Decimal.from_float(float(saved['acceleration'].ravel()[column])) for coefficient,column in zip(matrix.data[first:last],matrix.indices[first:last])),Decimal(0))
                    error = max(error,abs(value-Decimal.from_float(float(saved['force'].ravel()[row_index]))))
                evidence.check(prefix+':independent_mass_rows',float(error)/scale<2e-10,float(error)/scale)
                trace = saved['speed_square'][:,None]*saved['curvatures']+(saved['drift']+saved['source_acceleration'])[:,None]*saved['slopes']
                evidence.check(prefix+':source_trace_replay',np.array_equal(trace,saved['trace']))
                evidence.check(prefix+':shape_summary',float(np.max(abs(saved['shape_layers'])))==item['maximum_shape_force'])
                evidence.check(prefix+':integrated_shape_summary',float(np.max(abs(saved['weights']@saved['shape_layers'])))==item['integrated_shape_force_max'])
                if item['branch']=='reference':
                    evidence.check(prefix+':empty_native_reference',not np.any(saved['native_force']) and not np.any(saved['shape_layers']))
                if item['name'].startswith('iteration'):
                    state_row = next(row for row in live['states'] if row['name']==item['name'])
                else:
                    state_row = next(row for row in reversed(live['states']) if row['branch']==item['branch'])
                state = read_archive(evidence.root/state_row['path'])
                evidence.check(prefix+':state_owns_field',np.array_equal(saved['coordinates'],state['coordinates']))
                loads,action = restore_refined(live_base_action.owner,state,live_packet['mesh'],live_packet,item['branch'],deadline)
                cardinal = np.array([action.cardinal(label).ravel() for label in saved['labels']])
                source = cardinal@action.source
                metric_values,metric_derivatives = action.solver.values(action.solution,source)
                metric = 1-2*metric_values[0]/source
                metric_derivative = -2*metric_derivatives[0]/source+2*metric_values[0]/source**2
                geodesic_acceleration = -np.exp(2*metric_values[1])*metric*metric_derivatives[1]
                defect = saved['source_acceleration']-geodesic_acceleration
                curvature_defect = saved['curvatures']/saved['slopes']+(2/source+metric_derivative/(2*metric))[:,None]
                row = dict(name=item['name'],branch=item['branch'],material=item['material'],Euler_replay=relative,
                    source_trace_max=float(np.max(abs(trace))),point_relative=item['relative_point_residual'] if item['branch']=='primary' else 'not_applicable_empty_operator',
                    jump_relative=item['relative_jump_residual'] if item['branch']=='primary' else 'not_applicable_zero_native_load',jump_absolute=item['maximum_jump_residual'],
                    integrated_shape_max=item['integrated_shape_force_max'],acceleration_max=item['maximum_acceleration'],
                    geodesic_acceleration_defect=float(np.max(abs(defect))),geometric_curvature_defect=float(np.max(abs(curvature_defect))),valid_for_claim=False)
                live_rows.append(row)
                geodesic.append(dict(name=item['name'],geodesic_defect=row['geodesic_acceleration_defect'],curvature_defect=row['geometric_curvature_defect']))
                if item['name']=='primary-16-64':
                    coordinates_reference = saved['coordinates']
                if item['name']=='reference-16-64':
                    evidence.check('live:matched_initial_data_reference',np.array_equal(saved['coordinates'],coordinates_reference))
        for name,rows in [('carrier-validation',summary),('live-transmission-comparison',live_rows)]:
            path = evidence.output/(name+'.csv')
            with path.open('x',encoding='utf-8',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path,'outputs')
        evidence.report.update(seconds=perf_counter()-started,carrier_summary=summary,live_summary=live_rows,geodesic_comparison=geodesic,
            retained_failure_reconciled=True,continuous_material_proof=False,physical_evolution=False,github_action=False,subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
