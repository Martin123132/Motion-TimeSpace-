from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, live_refined
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_joint_first_tangent_20260922 import ZeroTangent, shifted_coordinates, ProbeMetricRate, RadialResponse, MomentumMetricResponse
from annular_joint_flow_derivative_v2_20260922 import solve_joint_rhs
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_moving_Legendre_current_20260921 import full_system
from annular_radial_Ward_moments_20260921 import KernelPrimitive, averaged_moments, prepare
from annular_local_current_commutators_20260922 import gram_pairs, layer_channels
from annular_transport_galerkin_20260922 import CHANNELS, TERMS, generator, evaluate_layer, decomposition
from annular_candidate_energy_current_20260921 import richardson
from annular_candidate_hamiltonian_20260921 import decimals
from scipy.sparse import save_npz
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',default='annular-resampled-parent-current-attempt01')
    parser.add_argument('--max-seconds',type=float,default=10000)
    parser.add_argument('--reuse')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label,__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        intake = evidence.output.parent
        names = ['reference-reference','MTS-primary','MTS-alternative']
        authority_names = ['annular-reference-matched-current-validation-attempt01',
            'annular-MTS-primary-matched-current-validation-attempt02',
            'annular-MTS-alternative-matched-current-validation-attempt01']
        digests = {}
        authorities = {}
        for folder in ['annular-resampled-parent-dynamics-preparation-attempt01',*authority_names]:
            path = intake/folder/'status.json'
            authority = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(folder+':complete',authority['state']=='complete' and all(row['passed'] for row in authority['checks']))
            authorities[folder] = authority
            for table in ['inputs','outputs']:
                for relative,digest in authority[table].items():
                    if relative in digests and digests[relative]!=digest:
                        raise RuntimeError('Conflicting source hash: '+relative)
                    digests[relative] = digest

        def owned(path):
            relative = str(path.relative_to(evidence.root))
            evidence.check(relative+':hash',relative in digests and hashlib.sha256(path.read_bytes()).hexdigest()==digests[relative])
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}

        def read_new(relative):
            path = evidence.root/relative
            evidence.check(relative+':new_hash',hashlib.sha256(path.read_bytes()).hexdigest()==evidence.report['outputs'][relative])
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}

        outer_steps = np.array([1e-4,5e-5,2.5e-5])
        inner_steps = np.array([7.8125e-7,3.90625e-7,1.953125e-7])
        evidence.own(evidence.root/'DERIVATION-20260923-resampled-parent-current.md')
        evidence.report.update(scientific_checks=[],iterations=[],summaries=[],centres=[],fine_summaries=[],
            outer_steps=outer_steps.tolist(),inner_steps=inner_steps.tolist(),branches=names,physical_time=0.,
            central_nonlinear_solves=0,new_nonlinear_solves=0,channels=CHANNELS,transport_terms=TERMS,
            all_interfaces_retained=True,pressure_adjusted=False,new_fitted_parameters=False,
            same_physical_interaction_support=True,github_action=False,subagents_used=False,
            outer_jet='q0+s*v0, v0+s*a0; own newly solved parent acceleration for each branch',
            maximum_seconds=args.max_seconds,protocol='resampled-parent-full-current-v1')
        reused = {}
        if args.reuse:
            path = intake/args.reuse/'status.json'
            prior = json.loads(path.read_text())
            evidence.own(path)
            evidence.check('reuse_same_protocol',prior['protocol']==evidence.report['protocol'] and prior['branches']==names
                and prior['outer_steps']==outer_steps.tolist() and prior['inner_steps']==inner_steps.tolist())
            digests.update(prior['inputs'])
            digests.update(prior['outputs'])
            reused = {row['case']:row for row in prior['cases'] if row.get('complete')}

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Saved time-budget boundary; completed case files retained')

        def save(label,**arrays):
            path = evidence.output/(label+'.npz')
            if path.exists():
                raise FileExistsError(str(path))
            np.savez_compressed(path,**arrays)
            evidence.own(path,'outputs')
            evidence.save()
            return str(path.relative_to(evidence.root))

        def science(case,quantity,error,tolerance):
            evidence.report['scientific_checks'].append(dict(case=case,quantity=quantity,error=float(error),tolerance=float(tolerance),
                passed=bool(np.isfinite(error) and error<=tolerance)))
            evidence.save()

        configurations,fine_radial = {},{}
        for name,authority_name in zip(names,authority_names):
            branch,extension = name.split('-')
            original = owned(intake/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(intake/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(intake/'annular-resampled-parent-dynamics-preparation-attempt01'/(name+'-parent-action.json'))
            initial = owned(evidence.root/packet['initial_source'])
            fine_packet = owned(evidence.root/packet['fine_action_source'])
            evidence.check(name+':parent_shape',packet['count']==1094 and initial['rates'].shape==(15,1095))
            evidence.check(name+':fixed_physical_interaction',packet['fixed_interaction_support']
                and packet['gram_support']==fine_packet['gram_support']
                and len(packet['gram_factor']['rows'])==len(fine_packet['gram_factor']['rows'])
                and len(packet['gram_sampling'])==len(fine_packet['gram_sampling'])
                and (bool(packet['gram_factor']['rows'])==(branch=='MTS')))
            evidence.check(name+':initial_t0',packet['physical_time']==0. and packet['route']=='resampled'
                and np.array_equal(np.asarray(initial['coordinates'][:,-1],float),original['coordinates'][:,-1])
                and np.array_equal(initial['rates'][:,-1],original['fixed_rates'][:,-1]))
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            base,unused,unused2 = common_material(native,original,overlay)
            configurations[name] = dict(owner=adapt_owner(base,packet['mesh']),packet=packet,initial=initial,extension=extension)
            fine_folder = 'annular-'+('reference' if branch=='reference' else name)+'-matched-current-attempt01'
            fine = owned(intake/fine_folder/'status.json')
            digests.update(fine['inputs'])
            digests.update(fine['outputs'])
            summary = next(row for row in fine['summaries'] if row['route']=='resampled')
            fine_radial[name] = [owned(evidence.root/path) for path in summary['radial_paths']]
            owned(evidence.root/summary['component_path'])
            evidence.report['fine_summaries'].append(dict(summary,branch=name,authority=authority_name))
        centres,results = {},{}
        tasks = [(name,index,sign) for name in names for index,sign in
            [(-1,0),*[(index,sign) for index in range(3) for sign in [-1,1]]]]
        for route,index,sign in tasks:
            config = configurations[route]
            owner,packet,extension = config['owner'],config['packet'],config['extension']
            case = route+'-parent-resampled-index'+str(index)+'-sign'+str(sign)
            if case in reused:
                row = reused[case]
                state,flow = owned(evidence.root/row['state_path']),owned(evidence.root/row['flow_path'])
                moments = [owned(evidence.root/path) for path in row['moment_paths']]
                for path in [*row['probe_paths'],*row['transport_quadrature_paths']]:
                    owned(evidence.root/path)
                matrix_path = evidence.root/row['matrix_path']
                relative = str(matrix_path.relative_to(evidence.root))
                evidence.check(case+':reused_matrix_hash',hashlib.sha256(matrix_path.read_bytes()).hexdigest()==digests[relative])
                evidence.own(matrix_path)
                results[route,index,sign] = dict(moments=moments,channels=owned(evidence.root/row['channel_path']),
                    transport=owned(evidence.root/row['transport_path']))
                evidence.report['cases'].append(dict(row,reused=True))
                if index==-1:
                    centres[route] = dict(state=state,flow=flow,moments=moments)
                    evidence.report['centres'].append(row)
                evidence.report['scientific_checks'].extend(item for item in prior['scientific_checks']
                    if item['case']==case or item['case'].startswith(case+'-'))
                for item in prior['iterations']:
                    if item['case']==case:
                        owned(evidence.root/item['output'])
                        evidence.report['iterations'].append(item)
                progress(case+'-reused')
                continue
            progress(case+'-start')
            if index==-1:
                duration = 0.
                coordinates,rates = decimals(config['initial']['coordinates']),config['initial']['rates'].copy()
            else:
                centre = centres[route]
                duration = sign*outer_steps[index]
                coordinates = shifted_coordinates(decimals(centre['state']['coordinates']),centre['state']['rates'],duration)
                rates = centre['state']['rates']+duration*centre['flow']['accelerations'][-1]
            loads, action = live_refined(owner,coordinates,rates,packet['mesh'],packet,extension,deadline)
            evidence.report['new_nonlinear_solves'] += 1
            if index==-1:
                evidence.report['central_nonlinear_solves'] += 1
            evidence.check(case+':nonlinear_constraint', action.solution['maximum_residual']<=2e-12, action.solution['maximum_residual'])
            state_path = save(case+'-state',coordinates=np.array(coordinates,dtype=str),rates=rates,edges=action.solver.edges,
                **{key:action.solution[key] for key in ['state','rhs_coefficients','primitives','left']})
            progress(case+'-metric-saved')
            system = full_system(action,ZeroTangent(),deadline,lambda stage:progress(case+'-'+stage))
            matrix_path = evidence.output/(case+'-Hessian.npz')
            save_npz(matrix_path,system['matrix'])
            evidence.own(matrix_path,'outputs')
            momentum = MomentumMetricResponse(action,deadline,lambda stage:progress(case+'-'+stage))
            evidence.check(case+':independent_momentum',np.max(abs(momentum.base_momentum()-system['momentum']))<=2e-15)
            probes, probe_paths = {}, []
            for inner_index, step in enumerate(inner_steps):
                for inner_sign in [-1,1]:
                    label = case+'-inner'+str(inner_index)+'-sign'+str(inner_sign)
                    progress(label)
                    shifted = shifted_coordinates(coordinates,rates,inner_sign*step)
                    local_loads, local_action = live_refined(owner,shifted,rates,packet['mesh'],packet,extension,deadline)
                    evidence.report['new_nonlinear_solves'] += 1
                    evidence.check(label+':constraint',local_action.solution['maximum_residual']<=2e-12)
                    probe_paths.append(save(label,coordinates=np.array(shifted,dtype=str),rates=rates,edges=local_action.solver.edges,
                        **{key:local_action.solution[key] for key in ['state','rhs_coefficients','primitives','left']}))
                    probes[inner_index,inner_sign] = local_action
            coordinate = ProbeMetricRate(probes,inner_steps)
            coordinate_momentum = np.array([momentum.accumulate(lambda radius:coordinate.values(radius)[estimate]) for estimate in range(2)])
            coordinate.cache.clear()
            response = RadialResponse(loads,action,extension,deadline,lambda stage:progress(case+'-'+stage))
            evidence.check(case+':radial_response_constraint',response.base_constraint_residual<=2e-12)
            accelerations, responses, couplings = [], [], []
            for estimate in range(2):
                def record(row, acceleration, coupling, residual, metric):
                    path = save(case+'-estimate'+str(estimate)+'-iteration'+str(row['iteration']),acceleration=acceleration,
                        coupling=coupling,residual=residual,forcing=metric.forcing,
                        **{'metric_'+key:value for key,value in metric.solution.items()})
                    evidence.report['iterations'].append(dict(row,case=case,estimate=estimate,output=path))
                rhs = system['force']-system['convection'][-1]-coordinate_momentum[estimate]
                acceleration, metric, coupling, unused, history = solve_joint_rhs(system,response,momentum,rhs,record)
                accelerations.append(acceleration)
                responses.append(metric)
                couplings.append(coupling)
            accelerations = np.array(accelerations)
            science(case,'paired_acceleration',np.max(abs(accelerations[1]-accelerations[0])),2e-8)
            tangent = JointMetricTangent(coordinate,responses)
            radius = np.linspace(action.solver.edges[0],action.solver.edges[-1],257)
            flow_path = save(case+'-flow',accelerations=accelerations,force=system['force'],momentum=system['momentum'],
                coordinate_convection=system['convection'][-1],coordinate_momentum=coordinate_momentum,coupling=np.array(couplings),
                radius=radius,metric_rate=tangent.values(radius),inner_steps=inner_steps)
            moments, moment_paths = [], []
            for spatial, material, kernel_order in [(8,48,16),(12,64,24)]:
                progress(case+'-moments'+str(spatial))
                kernel = KernelPrimitive(action,kernel_order)
                raw = averaged_moments(action,loads,tangent,kernel,accelerations[-1],spatial,material,deadline)
                moment_paths.append(save(case+'-moments'+str(spatial),**raw))
                moments.append(raw)
                for sector in ['wave','dust']:
                    science(case+'-moments'+str(spatial),sector+'_radial_identity',np.max(abs(raw['label_'+sector+'_identity_error'])),2e-11)
                coordinate.cache.clear()
            science(case,'paired_current_quadrature',np.max(abs(moments[1]['sum_horizontal']-moments[0]['sum_horizontal'])),2e-10)
            polynomial, unused = prepare(action,loads,accelerations[-1])
            pairs = gram_pairs(action)
            channels = []
            progress(case+'-local-channels')
            for label in moments[1]['labels']:
                channels.append(layer_channels(action,loads,tangent,kernel,accelerations[-1],polynomial,pairs,label))
                coordinate.cache.clear()
            packed = {key:np.array([row[key] for row in channels]) for key in channels[0]}
            summed = {key:np.tensordot(moments[1]['weights'],value,axes=(0,0)) for key,value in packed.items()}
            expected_wave = moments[1]['label_horizontal_wave']-(moments[1]['label_minimal']-moments[1]['label_dust_moment'])
            science(case,'wave_commutator_identity',np.max(abs(packed['predicted_wave']-expected_wave)),2e-16)
            science(case,'Gram_commutator_identity',np.max(abs(packed['predicted_gram']-moments[1]['label_horizontal_gram'])),2e-16)
            channel_path = save(case+'-channels',labels=moments[1]['labels'],weights=moments[1]['weights'],
                **packed,**{'sum_'+key:value for key,value in summed.items()})
            progress(case+'-allface-Galerkin-split')
            vertices, test_polynomial, test_image, cardinal_error = generator(action,loads,kernel)
            evidence.check(case+':material_cardinals',cardinal_error<=2e-12)
            flat_test = np.pad(vertices,((0,0),(0,0),(0,1))).reshape(3,-1)
            euler = system['force']-system['convection'][-1]-coordinate_momentum[-1]-couplings[-1]
            euler_work = flat_test@(euler.ravel()-system['matrix']@accelerations[-1].ravel())
            zero_mode, zero_polynomial = np.zeros_like(accelerations[-1]), np.zeros_like(polynomial)
            averages, transport_paths = [], []
            for order in [48,64]:
                labels, weights = np.polynomial.legendre.leggauss(order)
                labels, weights = labels/2, weights/2
                weights *= 6*(labels+.5)*(.5-labels)
                raw = []
                for label in labels:
                    values = evaluate_layer(action,loads,tangent,ZeroResponse(),kernel,accelerations[-1],polynomial,
                        zero_mode,zero_polynomial,vertices,test_polynomial,test_image,label)
                    raw.append(values[0])
                    coordinate.cache.clear()
                raw = np.array(raw)
                average = np.tensordot(weights,raw,axes=(0,0))
                evidence.check(case+':local_transport_split'+str(order),np.max(abs(raw[:,:6].sum(axis=1)-raw[:,8]-raw[:,9]))<=2e-16)
                transport_paths.append(save(case+'-transport-material'+str(order),labels=labels,weights=weights,values=raw,average=average))
                averages.append(average)
                progress(case+'-transport-material'+str(order)+'-saved')
            terms, weak_defect = decomposition(np.stack([averages[0]]*2),np.stack([averages[1]]*2),euler_work,np.zeros(3))
            terms, weak_defect = terms[0], weak_defect[0]
            actual = averages[1][8]+averages[1][9]
            expected = summed['components'][1]+summed['components'][2]
            science(case,'weak_Galerkin_assembly_identity',np.max(abs(weak_defect)),2e-16)
            science(case,'transport_current_replay',np.max(abs(actual-expected)),2e-16)
            science(case,'source_anchor_face_silence',np.max(abs(averages[1][10])),2e-16)
            evidence.check(case+':complete_transport_accounting',np.max(abs(terms.sum(axis=0)-actual))<=2e-16)
            transport_path = save(case+'-transport',terms=terms,averages=np.array(averages),actual=actual,expected=expected,
                full_Euler_work=euler_work,weak_defect=weak_defect,generator_vertices=vertices)
            results[route,index,sign] = dict(moments=moments,channels={'sum_components':summed['components']},transport={'terms':terms})
            evidence.report['cases'].append(dict(case=case,route=route,index=index,sign=sign,duration=duration,complete=True,
                state_path=state_path,flow_path=flow_path,matrix_path=str(matrix_path.relative_to(evidence.root)),probe_paths=probe_paths,
                moment_paths=moment_paths,channel_path=channel_path,transport_path=transport_path,transport_quadrature_paths=transport_paths,
                seconds=perf_counter()-started))
            if index==-1:
                centres[route] = dict(state=read_new(state_path),flow=read_new(flow_path),moments=moments)
                evidence.report['centres'].append(evidence.report['cases'][-1])
            progress(case+'-complete')
            del loads,action,system,momentum,probes,coordinate,response,tangent,responses,local_loads,local_action,kernel
            gc.collect()
        table, component_table, radial = [], [], {}
        for route in names:
            estimates, radial_paths = [], []
            for resolution in range(2):
                values = np.array([[results[route,index,sign]['moments'][resolution]['sum_horizontal'] for sign in [-1,1]] for index in range(3)])
                minimal = np.array([[results[route,index,sign]['moments'][resolution]['sum_minimal'] for sign in [-1,1]] for index in range(3)])
                derivative, minimal_derivative = richardson(values,outer_steps)[1], richardson(minimal,outer_steps)[1]
                center = centres[route]['moments'][resolution]
                spatial = center['sum_wave_space']+center['sum_gram_space']+center['sum_dust_space']
                source = center['sum_cell_source']+center['sum_face_source']+center['sum_endpoint_source']+center['sum_dust_euler']
                correction = derivative-minimal_derivative
                direct, predicted = derivative+spatial, source+center['sum_gram_space']+correction
                science(route+'-resolution'+str(resolution),'radial_decomposition',np.max(abs(direct-predicted)),2e-11)
                science(route+'-resolution'+str(resolution),'outer_radial_resolution',np.max(abs(direct[1]-direct[0])),2e-10)
                science(route+'-resolution'+str(resolution),'radial_zero_question',np.max(abs(direct[-1])),2e-10)
                radial_paths.append(save(route+'-resolution'+str(resolution)+'-radial',values=values,minimal_values=minimal,outer_steps=outer_steps,
                    derivative=derivative,minimal_derivative=minimal_derivative,spatial=spatial,minimal_source=source,
                    correction_rate=correction,direct=direct,predicted=predicted,gram_space=center['sum_gram_space']))
                estimates.append(direct)
            science(route,'paired_radial_quadrature',np.max(abs(estimates[1][-1]-estimates[0][-1])),2e-10)
            channel_values = np.array([[results[route,index,sign]['channels']['sum_components'] for sign in [-1,1]] for index in range(3)])
            transport_values = np.array([[results[route,index,sign]['transport']['terms'] for sign in [-1,1]] for index in range(3)])
            channel_rate, transport_rate = richardson(channel_values,outer_steps)[1], richardson(transport_values,outer_steps)[1]
            science(route,'local_channel_current_rate',np.max(abs(channel_rate.sum(axis=1)-correction)),2e-11)
            science(route,'transport_rate_replay',np.max(abs(transport_rate.sum(axis=1)-channel_rate[:,1]-channel_rate[:,2])),2e-11)
            science(route,'transport_rate_resolution',np.max(abs(transport_rate[1]-transport_rate[0])),2e-10)
            source_names = ['cell_source','face_source','endpoint_source','dust_euler','gram_space']
            component_names = source_names+['current_interpolation','current_endpoint','current_gram_bond','current_gram_geometry','current_gram_advection']+['transport_'+name for name in TERMS]
            constants = np.array([center['sum_'+name] for name in source_names])
            components = np.concatenate([np.stack([constants]*2),channel_rate[:,[0,3,4,5,6]],transport_rate],axis=1)
            science(route,'whole_component_accounting',np.max(abs(components.sum(axis=1)-estimates[1])),2e-11)
            path = save(route+'-component-rates',channel_values=channel_values,transport_values=transport_values,channel_rate=channel_rate,
                transport_rate=transport_rate,components=components,component_names=np.array(component_names),steps=outer_steps,
                radial=np.array(estimates),outer_change=abs(estimates[1][1]-estimates[1][0]),quadrature_change=abs(estimates[1][-1]-estimates[0][-1]))
            radial[route] = np.array(estimates)
            evidence.report['summaries'].append(dict(route=route,radial_paths=radial_paths,component_path=path,
                signed_radial=estimates[1][-1].tolist(),trace_lift_rate=transport_rate[-1,1].tolist(),
                outer_change=abs(estimates[1][1]-estimates[1][0]).tolist(),quadrature_change=abs(estimates[1][-1]-estimates[0][-1]).tolist()))
            for component, component_name in enumerate(component_names):
                for test in range(3):
                    component_table.append(dict(route=route,component=component_name,test=test,value=components[-1,component,test],
                        paired_change=abs(components[1,component,test]-components[0,component,test])))
        for route in names:
            coarse = radial[route]
            fine = np.array([row['direct'] for row in fine_radial[route]])
            coarse_summary = next(row for row in evidence.report['summaries'] if row['route']==route)
            with np.load(evidence.root/coarse_summary['radial_paths'][1],allow_pickle=False) as saved:
                coarse_gap = saved['direct'][-1]-saved['predicted'][-1]
            fine_gap = fine_radial[route][1]['direct'][-1]-fine_radial[route][1]['predicted'][-1]
            for test in range(3):
                before,after = coarse[1,-1,test],fine[1,-1,test]
                table.append(dict(branch=route,test=test,parent=before,fine=after,change=after-before,
                    absolute_ratio=abs(after/before) if before else None,
                    parent_outer_change=abs(coarse[1,1,test]-coarse[1,0,test]),
                    fine_outer_change=abs(fine[1,1,test]-fine[1,0,test]),
                    parent_quadrature_change=abs(coarse[1,-1,test]-coarse[0,-1,test]),
                    fine_quadrature_change=abs(fine[1,-1,test]-fine[0,-1,test]),
                    parent_decomposition_gap=coarse_gap[test],fine_decomposition_gap=fine_gap[test]))
        for filename,rows in [('parent-fine-radial.csv',table),('complete-component-rates.csv',component_table)]:
            path = evidence.output/filename
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path,'outputs')
        evidence.report.update(seconds=perf_counter()-started,science_passed=sum(row['passed'] for row in evidence.report['scientific_checks']),
            science_total=len(evidence.report['scientific_checks']),comparison=table,full_radial_comparison_completed=True,
            mesh_levels=2,asymptotic_convergence_order_established=False)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],comparison=table)),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
