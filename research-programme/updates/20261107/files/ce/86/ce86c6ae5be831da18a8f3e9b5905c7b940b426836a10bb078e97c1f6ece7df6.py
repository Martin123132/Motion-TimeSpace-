from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_joint_first_tangent_20260922 import RadialResponse, MomentumMetricResponse, ProbeMetricRate
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_joint_flow_derivative_v2_20260922 import DecimalSparseResidual
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_radial_Ward_moments_20260921 import KernelPrimitive, prepare, averaged_moments
from annular_interface_jump_evolution_20260922 import layer as endpoint_layer
from scipy.sparse import load_npz
from types import SimpleNamespace
from decimal import Decimal, localcontext
from datetime import datetime, timezone
from time import perf_counter
import argparse
import contextlib
import csv
import gc
import hashlib
import json
import numpy as np


class ZeroResponse:
    def values(self, radius):
        return np.zeros((2, len(radius)))


def independent_derivative(values, steps):
    shape = values.shape[2:]
    packed = values.reshape(3,2,-1)
    result = np.empty((2,packed.shape[-1]))
    with localcontext() as context:
        context.prec = 64
        for column in range(packed.shape[-1]):
            slopes = [(Decimal.from_float(float(packed[index,1,column]))-Decimal.from_float(float(packed[index,0,column])))
                /(2*Decimal.from_float(float(steps[index]))) for index in range(3)]
            for estimate in range(2):
                result[estimate,column] = float((4*slopes[estimate+1]-slopes[estimate])/3)
    return result.reshape((2,)+shape)


def independent_shift(coordinates, rates, duration):
    output = np.empty(coordinates.shape,dtype=object)
    with localcontext() as context:
        context.prec = 64
        step = Decimal.from_float(float(duration))
        for index in np.ndindex(coordinates.shape):
            output[index] = Decimal(str(coordinates[index]))+step*Decimal.from_float(float(rates[index]))
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run',default='annular-resampled-parent-current-attempt01')
    parser.add_argument('--label',default='annular-resampled-parent-current-validation-attempt01')
    parser.add_argument('--protected-since',default='2026-09-23T15:04:37+00:00')
    parser.add_argument('--max-seconds',type=float,default=4200)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        intake = evidence.output.parent
        main_path = intake/args.run/'status.json'
        parent = json.loads(main_path.read_text())
        evidence.own(main_path)
        names = ['reference-reference','MTS-primary','MTS-alternative']
        evidence.check('main_complete',parent['state']=='complete' and all(row['passed'] for row in parent['checks']))
        evidence.check('fixed_protocol',parent['protocol']=='resampled-parent-full-current-v1' and parent['branches']==names
            and parent['physical_time']==0. and parent['all_interfaces_retained'] and parent['same_physical_interaction_support']
            and not parent['valid_for_physics_claim'] and not parent['asymptotic_convergence_order_established'])
        digests = dict(parent['inputs'],**parent['outputs'])
        for relative,digest in digests.items():
            path = evidence.root/relative
            evidence.check(relative+':hash',path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest)
            evidence.own(path)

        def read(path):
            relative = str(path.relative_to(evidence.root))
            evidence.check(relative+':registered',relative in digests)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}

        def save(label,**arrays):
            path = evidence.output/(label+'.npz')
            if path.exists():
                raise FileExistsError(str(path))
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            evidence.save()
            return str(path.relative_to(evidence.root))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Saved validator runtime boundary')

        configurations,centres = {},{}
        for name in names:
            branch,extension = name.split('-')
            original = read(intake/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = read(intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = read(intake/'annular-resampled-parent-dynamics-preparation-attempt01'/(name+'-parent-action.json'))
            fine_packet = read(evidence.root/packet['fine_action_source'])
            initial = read(evidence.root/packet['initial_source'])
            evidence.check(name+':fixed_interaction_support',packet['extension']==extension
                and packet['fixed_interaction_support'] and packet['gram_support']==fine_packet['gram_support']
                and len(packet['gram_factor']['rows'])==len(fine_packet['gram_factor']['rows'])
                and len(packet['gram_sampling'])==len(fine_packet['gram_sampling'])
                and (bool(packet['gram_factor']['rows'])==(branch=='MTS')))
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            base,unused,unused2 = common_material(native,original,overlay)
            configurations[name] = dict(owner=adapt_owner(base,packet['mesh']),packet=packet,extension=extension,initial=initial)
            row = next(row for row in parent['centres'] if row['route']==name)
            evidence.check(name+':independently_solved_centre',row['index']==-1 and row['sign']==0 and row['duration']==0. and row['complete'])
            centres[name] = dict(state=read(evidence.root/row['state_path']),flow=read(evidence.root/row['flow_path']),
                moments=[read(evidence.root/path) for path in row['moment_paths']])
        expected_keys = {(route,index,sign) for route in names for index,sign in
            [(-1,0),*[(index,sign) for index in range(3) for sign in [-1,1]]]}
        evidence.check('twenty_one_unique_centre_outer_states',len(parent['cases'])==21 and len(parent['centres'])==3 and
            {(row['route'],row['index'],row['sign']) for row in parent['cases']}==expected_keys)
        evidence.report.update(branches=names,scientific_replays=[],maximum_seconds=args.max_seconds,
            github_action=False,subagents_used=False,all_faces_independently_replayed=True,independent_centres=3)
        values,results,traces = {},{},{}
        for row in parent['cases']:
            case,route,index,sign = [row[key] for key in ['case','route','index','sign']]
            progress(case+'-fresh-operator-check')
            state,flow = read(evidence.root/row['state_path']),read(evidence.root/row['flow_path'])
            config = configurations[route]
            owner,packet,extension = config['owner'],config['packet'],config['extension']
            centre = centres[route]
            actual_q = np.array([[Decimal(value) for value in line] for line in state['coordinates']])
            if index==-1:
                expected_q = np.array([[Decimal(value) for value in line] for line in config['initial']['coordinates']])
                expected_v = config['initial']['rates']
            else:
                duration = sign*parent['outer_steps'][index]
                expected_q = independent_shift(centre['state']['coordinates'],centre['state']['rates'],duration)
                expected_v = centre['state']['rates']+duration*centre['flow']['accelerations'][-1]
            evidence.check(case+':own_centre_phase_jet',np.array_equal(actual_q,expected_q) and np.array_equal(state['rates'],expected_v))
            evidence.check(case+':all_coordinates_retained',state['rates'].shape==(15,1095) and state['rates'].size==16425)
            loads,action = restore_refined(owner,state,packet['mesh'],packet,extension,deadline)
            response = RadialResponse(loads,action,extension,deadline,lambda stage:None)
            evidence.check(case+':fresh_radial_constraint',response.base_constraint_residual<=2e-12,response.base_constraint_residual)
            momentum = MomentumMetricResponse(action,deadline,lambda stage:None)
            evidence.check(case+':fresh_momentum',np.max(abs(momentum.base_momentum()-flow['momentum']))<=2e-15)
            matrix = load_npz(evidence.root/row['matrix_path'])
            evidence.check(case+':full_Hessian_dimension',matrix.shape==(16425,16425))
            inverse = BandedSourceInverse(matrix,state['rates'].shape)
            arithmetic = DecimalSparseResidual(matrix)
            probes = {}
            evidence.check(case+':six_inner_probes',len(row['probe_paths'])==6)
            for inner_index in range(3):
                for inner_sign in [-1,1]:
                    suffix = '-inner'+str(inner_index)+'-sign'+str(inner_sign)+'.npz'
                    path = next(evidence.root/path for path in row['probe_paths'] if path.endswith(suffix))
                    archive = read(path)
                    shifted = independent_shift(state['coordinates'],state['rates'],inner_sign*flow['inner_steps'][inner_index])
                    archived_q = np.array([[Decimal(value) for value in line] for line in archive['coordinates']])
                    evidence.check(case+suffix+':coordinate_only',np.array_equal(archived_q,shifted) and np.array_equal(archive['rates'],state['rates']))
                    solver,solution = reconstructed_solver(archive)
                    probes[inner_index,inner_sign] = SimpleNamespace(solver=solver,solution=solution)
            coordinate = ProbeMetricRate(probes,flow['inner_steps'])
            responses = []
            for estimate in range(2):
                replay = momentum.accumulate(lambda radius:coordinate.values(radius)[estimate])
                evidence.check(case+':fresh_coordinate_momentum'+str(estimate),np.max(abs(replay-flow['coordinate_momentum'][estimate]))<=2e-15)
                coordinate.cache.clear()
                acceleration = flow['accelerations'][estimate]
                fresh = response.apply(acceleration)
                coupling = momentum.accumulate(fresh.values)
                responses.append(fresh)
                evidence.check(case+':fresh_coupling'+str(estimate),np.max(abs(coupling-flow['coupling'][estimate]))<=2e-15)
                evidence.check(case+':linear_response'+str(estimate),fresh.residual<=2e-12,fresh.residual)
                rhs = flow['force']-flow['coordinate_convection']-flow['coordinate_momentum'][estimate]
                residual = arithmetic.evaluate(acceleration,coupling,rhs)
                relative = inverse.residual_norm(residual)/max(inverse.residual_norm(rhs),1e-30)
                correction = float(np.max(abs(inverse.solve(residual.ravel()))))
                evidence.check(case+':coupled_relative'+str(estimate),relative<=2e-11,relative)
                evidence.check(case+':coupled_correction'+str(estimate),correction<=2e-12,correction)
                final = max((entry for entry in parent['iterations'] if entry['case']==case and entry['estimate']==estimate),key=lambda entry:entry['iteration'])
                saved = read(evidence.root/final['output'])
                evidence.check(case+':final_acceleration'+str(estimate),np.array_equal(saved['acceleration'],acceleration))
                evidence.check(case+':saved_residual'+str(estimate),np.max(abs(saved['residual']-residual))<=2e-15)
            tangent = JointMetricTangent(coordinate,responses)
            evidence.check(case+':fresh_metric_jet',np.max(abs(tangent.values(flow['radius'])-flow['metric_rate']))<=2e-18)
            coordinate.cache.clear()
            moments = [read(evidence.root/path) for path in row['moment_paths']]
            channels = read(evidence.root/row['channel_path'])
            transport = read(evidence.root/row['transport_path'])
            quadratures = [read(evidence.root/path) for path in row['transport_quadrature_paths']]
            for order,raw in zip([8,12],moments):
                for key in raw:
                    if key.startswith('label_'):
                        target = raw['sum_'+key[6:]]
                        evidence.check(case+':weighted_moment'+str(order)+':'+key,np.max(abs(raw['weights']@raw[key]-target))<=2e-16)
                for sector in ['wave','dust']:
                    values[case+'-moments'+str(order),sector+'_radial_identity'] = np.max(abs(raw['label_'+sector+'_identity_error']))
            values[case,'paired_acceleration'] = np.max(abs(flow['accelerations'][1]-flow['accelerations'][0]))
            values[case,'paired_current_quadrature'] = np.max(abs(moments[1]['sum_horizontal']-moments[0]['sum_horizontal']))
            expected_wave = moments[1]['label_horizontal_wave']-moments[1]['label_minimal']+moments[1]['label_dust_moment']
            values[case,'wave_commutator_identity'] = np.max(abs(channels['predicted_wave']-expected_wave))
            values[case,'Gram_commutator_identity'] = np.max(abs(channels['predicted_gram']-moments[1]['label_horizontal_gram']))
            for key in ['components','predicted_wave','predicted_gram','predicted_total']:
                evidence.check(case+':weighted_channel:'+key,np.max(abs(np.tensordot(channels['weights'],channels[key],axes=(0,0))-channels['sum_'+key]))<=2e-16)
            averages = []
            for order,raw in zip([48,64],quadratures):
                average = np.tensordot(raw['weights'],raw['values'],axes=(0,0))
                evidence.check(case+':weighted_transport'+str(order),np.max(abs(average-raw['average']))<=2e-16)
                evidence.check(case+':local_transport'+str(order),np.max(abs(raw['values'][:,:6].sum(axis=1)-raw['values'][:,8]-raw['values'][:,9]))<=2e-16)
                averages.append(average)
            flat_test = np.pad(transport['generator_vertices'],((0,0),(0,0),(0,1))).reshape(3,-1)
            euler_residual = flow['force']-flow['coordinate_convection']-flow['coordinate_momentum'][-1]-flow['coupling'][-1]
            euler_work = flat_test@(euler_residual.ravel()-matrix@flow['accelerations'][-1].ravel())
            evidence.check(case+':independent_Euler_work',np.max(abs(euler_work-transport['full_Euler_work']))<=2e-16)
            weak = averages[0][4]+averages[0][5]-euler_work-averages[0][6]+averages[0][7]
            terms = np.stack([averages[1][0],averages[1][1],averages[1][2],averages[1][3],averages[0][6],-averages[0][7],
                euler_work,np.zeros(3),averages[1][4]+averages[1][5]-averages[0][4]-averages[0][5],weak])
            evidence.check(case+':all_ten_terms_reconstructed',np.max(abs(terms-transport['terms']))<=2e-16)
            values[case,'weak_Galerkin_assembly_identity'] = np.max(abs(weak))
            values[case,'transport_current_replay'] = np.max(abs(averages[1][8]+averages[1][9]-channels['sum_components'][1]-channels['sum_components'][2]))
            values[case,'source_anchor_face_silence'] = np.max(abs(averages[1][10]))
            evidence.check(case+':complete_transport',np.max(abs(terms.sum(axis=0)-averages[1][8]-averages[1][9]))<=2e-16)
            if index==2 and sign==1:
                for order,material,kernel_order,saved in zip([8,12],[48,64],[16,24],moments):
                    progress(case+'-fresh-moments'+str(order))
                    kernel = KernelPrimitive(action,kernel_order)
                    fresh = averaged_moments(action,loads,tangent,kernel,flow['accelerations'][-1],order,material,deadline)
                    for key in saved:
                        evidence.check(case+':fresh_moment'+str(order)+':'+key,np.max(abs(fresh[key]-saved[key]))<=2e-16)
                    coordinate.cache.clear()
            progress(case+'-independent-allface-trace')
            kernel = KernelPrimitive(action,24)
            polynomial,unused = prepare(action,loads,flow['accelerations'][-1])
            zero = np.zeros_like(flow['accelerations'][-1])
            traces_by_label, faces_by_label, pins_by_label = [], [], []
            for label in quadratures[1]['labels']:
                local = endpoint_layer(action,tangent,ZeroResponse(),kernel,None,flow['accelerations'][-1],polynomial,zero,np.zeros_like(polynomial),label)
                traces_by_label.append(local['trace'][0])
                pins_by_label.append(local['pin'][0])
                faces_by_label.append(local['psi']/2*(local['moments'][0,1:,0]-local['moments'][0,:-1,1]))
                coordinate.cache.clear()
            trace_rows, face_rows, pin_rows = np.array(traces_by_label),np.array(faces_by_label),np.array(pins_by_label)
            weights = quadratures[1]['weights']
            evidence.check(case+':independent_trace_lift_each_label',np.max(abs(trace_rows-quadratures[1]['values'][:,1]))<=2e-16)
            all_faces, trace, pin = np.tensordot(weights,face_rows,axes=(0,0)), weights@trace_rows, weights@pin_rows
            evidence.check(case+':allface_trace_closure',np.max(abs(all_faces.sum(axis=1)+pin-trace))<=2e-16)
            evidence.check(case+':trace_from_Galerkin_terms',np.max(abs(trace-transport['terms'][1]))<=2e-16)
            face_positions = np.array([float(value) for value in action.edges])[1:-1]
            evidence.check(case+':every_face_saved',all_faces.shape==(3,len(face_positions))
                and len(face_positions)==len(packet['mesh']['edges'])-2)
            trace_path = save(case+'-allface-trace',faces=face_positions,weighted_faces=all_faces,trace=trace,pin=pin,
                labels=quadratures[1]['labels'],weights=weights,label_traces=trace_rows,label_pins=pin_rows)
            traces[route,index,sign] = dict(faces=all_faces,pin=pin,positions=face_positions)
            results[route,index,sign] = dict(moments=moments,channels=channels,transport=transport)
            evidence.report['cases'].append(dict(case=case,allface_path=trace_path,maximum_fresh_radial_response=max(response.residuals),
                face_count=len(face_positions),seconds=perf_counter()-started))
            evidence.save()
            del loads,action,response,momentum,matrix,inverse,arithmetic,probes,coordinate,tangent,responses,kernel
            gc.collect()
        steps = np.array(parent['outer_steps'])
        comparisons,radials,component_rows,face_table = [],{},{},[]
        for summary in parent['summaries']:
            route = summary['route']
            estimates = []
            for resolution in range(2):
                saved = read(evidence.root/summary['radial_paths'][resolution])
                current = np.array([[results[route,index,sign]['moments'][resolution]['sum_horizontal'] for sign in [-1,1]] for index in range(3)])
                minimal = np.array([[results[route,index,sign]['moments'][resolution]['sum_minimal'] for sign in [-1,1]] for index in range(3)])
                derivative,minimal_rate = independent_derivative(current,steps),independent_derivative(minimal,steps)
                centre = centres[route]['moments'][resolution]
                spatial = centre['sum_wave_space']+centre['sum_gram_space']+centre['sum_dust_space']
                source = centre['sum_cell_source']+centre['sum_face_source']+centre['sum_endpoint_source']+centre['sum_dust_euler']
                correction = derivative-minimal_rate
                direct,predicted = derivative+spatial,source+centre['sum_gram_space']+correction
                for key,target in [('values',current),('minimal_values',minimal),('derivative',derivative),('minimal_derivative',minimal_rate),
                                   ('spatial',spatial),('minimal_source',source),('correction_rate',correction),('direct',direct),('predicted',predicted)]:
                    evidence.check(route+':independent_radial'+str(resolution)+':'+key,np.max(abs(saved[key]-target))<=2e-14)
                values[route+'-resolution'+str(resolution),'radial_decomposition'] = np.max(abs(direct-predicted))
                values[route+'-resolution'+str(resolution),'outer_radial_resolution'] = np.max(abs(direct[1]-direct[0]))
                values[route+'-resolution'+str(resolution),'radial_zero_question'] = np.max(abs(direct[-1]))
                estimates.append(direct)
            values[route,'paired_radial_quadrature'] = np.max(abs(estimates[1][-1]-estimates[0][-1]))
            saved = read(evidence.root/summary['component_path'])
            channel_data = np.array([[results[route,index,sign]['channels']['sum_components'] for sign in [-1,1]] for index in range(3)])
            transport_data = np.array([[results[route,index,sign]['transport']['terms'] for sign in [-1,1]] for index in range(3)])
            channel_rate,transport_rate = independent_derivative(channel_data,steps),independent_derivative(transport_data,steps)
            evidence.check(route+':independent_channel_rates',np.max(abs(channel_rate-saved['channel_rate']))<=2e-14)
            evidence.check(route+':independent_transport_rates',np.max(abs(transport_rate-saved['transport_rate']))<=2e-14)
            values[route,'local_channel_current_rate'] = np.max(abs(channel_rate.sum(axis=1)-correction))
            values[route,'transport_rate_replay'] = np.max(abs(transport_rate.sum(axis=1)-channel_rate[:,1]-channel_rate[:,2]))
            values[route,'transport_rate_resolution'] = np.max(abs(transport_rate[1]-transport_rate[0]))
            constants = np.array([centre['sum_'+key] for key in ['cell_source','face_source','endpoint_source','dust_euler','gram_space']])
            components = np.concatenate([np.stack([constants]*2),channel_rate[:,[0,3,4,5,6]],transport_rate],axis=1)
            values[route,'whole_component_accounting'] = np.max(abs(components.sum(axis=1)-estimates[1]))
            evidence.check(route+':complete_component_replay',np.max(abs(components-saved['components']))<=2e-14)
            component_rows[route] = (saved['component_names'],components)
            face_data = np.array([[traces[route,index,sign]['faces'] for sign in [-1,1]] for index in range(3)])
            pin_data = np.array([[traces[route,index,sign]['pin'] for sign in [-1,1]] for index in range(3)])
            face_rate,pin_rate = independent_derivative(face_data,steps),independent_derivative(pin_data,steps)
            evidence.check(route+':independent_allface_rate',np.max(abs(face_rate.sum(axis=2)+pin_rate-transport_rate[:,1]))<=2e-11)
            positions = traces[route,0,-1]['positions']
            for index in range(3):
                for sign in [-1,1]:
                    evidence.check(route+':fixed_reference_interfaces'+str(index)+str(sign),np.array_equal(positions,traces[route,index,sign]['positions']))
            save(route+'-independent-rates',radial=np.array(estimates),channel_rate=channel_rate,transport_rate=transport_rate,
                components=components,face_rate=face_rate,pin_rate=pin_rate,faces=positions)
            for face,position in enumerate(positions):
                for test in range(3):
                    face_table.append(dict(route=route,reference_face=position,test=test,trace_lift_rate=face_rate[-1,test,face],
                        paired_change=abs(face_rate[1,test,face]-face_rate[0,test,face])))
            radials[route] = np.array(estimates)
        for flag in parent['scientific_checks']:
            key = flag['case'],flag['quantity']
            evidence.check('science_has_independent_replay:'+str(key),key in values)
            value = float(values[key])
            passed = bool(np.isfinite(value) and value<=flag['tolerance'])
            evidence.check('science_flag_preserved:'+str(key),passed==flag['passed'] and abs(value-flag['error'])<=2e-14,
                dict(replayed=value,saved=flag['error'],scientific_passed=passed))
            evidence.report['scientific_replays'].append(dict(flag,replayed_error=value))
        evidence.check('no_scientific_flags_skipped',len(values)==len(parent['scientific_checks']))
        for route in names:
            fine_summary = next(row for row in parent['fine_summaries'] if row['branch']==route)
            fine_data = [read(evidence.root/path) for path in fine_summary['radial_paths']]
            fine = np.array([row['direct'] for row in fine_data])
            coarse = radials[route]
            summary = next(row for row in parent['summaries'] if row['route']==route)
            coarse_data = read(evidence.root/summary['radial_paths'][1])
            coarse_gap = coarse_data['direct'][-1]-coarse_data['predicted'][-1]
            fine_gap = fine_data[1]['direct'][-1]-fine_data[1]['predicted'][-1]
            for test in range(3):
                before,after = coarse[1,-1,test],fine[1,-1,test]
                comparisons.append(dict(branch=route,test=test,parent=before,fine=after,change=after-before,
                    absolute_ratio=abs(after/before) if before else None,
                    parent_outer_change=abs(coarse[1,1,test]-coarse[1,0,test]),
                    fine_outer_change=abs(fine[1,1,test]-fine[1,0,test]),
                    parent_quadrature_change=abs(coarse[1,-1,test]-coarse[0,-1,test]),
                    fine_quadrature_change=abs(fine[1,-1,test]-fine[0,-1,test]),
                    parent_decomposition_gap=coarse_gap[test],fine_decomposition_gap=fine_gap[test]))
        for filename,count in [('parent-fine-radial.csv',9),('complete-component-rates.csv',180)]:
            with (intake/args.run/filename).open(newline='',encoding='utf-8') as stream:
                rows = list(csv.DictReader(stream))
            evidence.check(filename+':clean_rows',len(rows)==count and all(None not in row and None not in row.values() for row in rows))
            if count==9:
                for row,expected in zip(rows,comparisons):
                    for key,target in expected.items():
                        if key=='branch':
                            valid = row[key]==target
                        elif target is None:
                            valid = row[key]==''
                        else:
                            tolerance = 2e-5 if key=='absolute_ratio' else 2e-14
                            valid = abs(float(row[key])-target)<=tolerance
                        evidence.check(filename+':'+row['branch']+':'+row['test']+':'+key,valid)
            else:
                for row in rows:
                    component_names,components = component_rows[row['route']]
                    selected = list(component_names).index(row['component'])
                    test = int(row['test'])
                    evidence.check(filename+':'+row['route']+':'+row['component']+':'+row['test'],
                        abs(float(row['value'])-components[-1,selected,test])<=2e-14
                        and abs(float(row['paired_change'])-abs(components[1,selected,test]-components[0,selected,test]))<=2e-14)
        for filename,rows in [('independent-comparison.csv',comparisons),('allface-trace-rates.csv',face_table)]:
            path = evidence.output/filename
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path,'outputs')
        threshold = datetime.fromisoformat(args.protected_since).timestamp()
        changed = [str(path) for path in (evidence.root.parent/'formalization-workbench').rglob('*') if path.is_file() and path.stat().st_mtime>=threshold]
        evidence.check('protected_workbench_unchanged',not changed,changed)
        evidence.check('no_scripts_bytecode_cache',not (evidence.root/'scripts/__pycache__').exists())
        for relative,digest in evidence.report['inputs'].copy().items():
            evidence.check('final_hash:'+relative,hashlib.sha256((evidence.root/relative).read_bytes()).hexdigest()==digest)
        evidence.report.update(seconds=perf_counter()-started,comparison=comparisons,science_passed=parent['science_passed'],
            science_total=parent['science_total'],scientific_false_flags=[row for row in parent['scientific_checks'] if not row['passed']],
            protected_workbench_changed_count=len(changed),
            validation_scope='Independent Decimal outer derivatives; 21 fresh coupled operators; all parent faces; fresh finest-positive currents on all three branches')
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],checks=len(evidence.report['checks']),comparison=comparisons)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
