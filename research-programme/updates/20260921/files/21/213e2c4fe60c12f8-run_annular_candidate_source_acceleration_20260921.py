from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_source_acceleration_20260921 import source_samples, symbolic_controls, analyze_probes, centered
from annular_candidate_midpoint_20260921 import LiveCommonEvaluation, advance_coordinates
from annular_endpoint_legendre_inverse_20260921 import endpoint_inverse
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from derive_annular_candidate_midpoint_20260921 import saved_matrix
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import contextlib
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds', type=float, default=9000)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-candidate-source-acceleration-attempt01', __file__)
    started = perf_counter()
    deadline = started+args.max_seconds
    try:
        prior_path = evidence.output.parent/'annular-candidate-finer-time-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('source_complete_and_finest_time_and_quadrature_qualified', prior['state'] == 'complete'
            and prior['finest_time_grid_qualified'] and prior['matched_quadrature_qualified']
            and all(row['passed'] for row in prior['checks']))
        evidence.report.update(github_action=False, subagents_used=False, original_action_unchanged=True,
            full_components=16425, modes_deleted=False, inverse_function_directional_derivative=True,
            prior_coarser_failed_gates_retained=True, maximum_seconds=args.max_seconds,
            reference_order=16, material_order=48, derivative_steps=[1e-5,5e-6,2.5e-6],
            numerical_derivative_relative_gate=2e-3, numerical_derivative_absolute_gate=1e-8,
            iterations=[], probes=[], derivative_checks=[], tangent_checks=[], samples=[],
            physical_acceleration_qualified=False, geodesic_match_claimed=False, newton_proxy_is_not_general_GR_prediction=True)
        symbolic_controls(evidence)

        def load_owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key, prior['outputs'].get(key))
            evidence.check(path.name+'_sealed_hash', expected is not None
                and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
            evidence.own(path)
            with np.load(path, allow_pickle=False) as data:
                return {name:data[name].copy() for name in data.files}

        run_path = evidence.output.parent/'annular-candidate-fine16-quadrature-attempt01/status.json'
        source_run = json.loads(run_path.read_text())
        evidence.own(run_path)
        for branch, extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, unused, unused_rates = common_material(native, saved, packet)
            action = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
            preconditioner = BandedSourceInverse(saved_matrix(evidence, case+'-22-fixed-metric-mass.npz'), (15,1095))
            evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline,
                reference_order=16, material_order=48)
            evidence.check(case+'_all_mass_directions', preconditioner.count == 16425
                and preconditioner.minimum_diagonal > 0 and preconditioner.minimum_schur_eigenvalue > 0)
            endpoint_row = next(row for row in source_run['endpoints'] if row['branch'] == branch
                and row['extension'] == extension and row['label'] == 'fine')
            initial_path = evidence.output.parent/'annular-candidate-midpoint-quadrature-attempt01'/(case+'-initial.npz')
            endpoint_path = evidence.root/endpoint_row['path']
            for label, state_path in [('initial',initial_path),('endpoint',endpoint_path)]:
                data = load_owned(state_path)
                position = decimals(data['coordinates'])
                momentum = decimals(data['momenta'] if label == 'initial' else data['target_momenta'])
                rates = data['midpoint_rates'] if label == 'initial' else data['endpoint_rates']
                name = case+'-'+label
                current = evaluator.evaluate(position,rates)
                with localcontext() as context:
                    context.prec = 64
                    residual = np.asarray(decimal_array(current['momentum'])-momentum,float)
                correction = preconditioner.solve(residual.ravel()).reshape(rates.shape)
                relative = preconditioner.residual_norm(residual)/preconditioner.residual_norm(np.asarray(momentum,float))
                evidence.check(name+'_base_inverse_and_chart', relative < 5e-12 and np.max(abs(correction)) < 2e-12
                    and current['radial_residual'] < 2e-12 and current['minimum_F'] > 0 and current['maximum_speed_ratio'] < 1)
                base = source_samples(owner,position,rates,current)
                force = current['force_decimal']
                base_path = evidence.output/(name+'-base.npz')
                np.savez_compressed(base_path, coordinates=np.asarray(position,str), momenta=np.asarray(momentum,str),
                    rates=rates, force_decimal=np.asarray(force,str), computed_momentum=current['momentum'],
                    preconditioned_residual=correction, radial_edges=current['solver'].edges,
                    radial_state=current['solution']['state'], **base)
                evidence.own(base_path,'outputs')
                evidence.report['cases'].append(dict(branch=branch,extension=extension,label=label,
                    path=str(base_path.relative_to(evidence.root)), source_path=str(state_path.relative_to(evidence.root)),
                    relative_residual=relative, maximum_correction=float(np.max(abs(correction))), valid_for_claim=False))
                evidence.save()
                probes = {}
                steps = evidence.report['derivative_steps']
                for index, step in enumerate(steps):
                    for sign in [1,-1]:
                        probe_name = name+'-probe'+str(index)+('-plus' if sign == 1 else '-minus')
                        displaced = advance_coordinates(position,rates,sign*step,64)
                        with localcontext() as context:
                            context.prec = 64
                            target = momentum+Decimal.from_float(sign*step)*force
                        def record(row, fixed, trial_rates, evaluated, trial_residual):
                            evidence.report['iterations'].append(dict(case=probe_name,**row,valid_for_claim=False))
                            evidence.report['progress'] = dict(case=probe_name,iteration=row['iteration'],seconds=perf_counter()-started)
                            np.savez_compressed(evidence.output/'latest-trial-recovery.npz', coordinates=np.asarray(fixed,str),
                                momenta=np.asarray(target,str), rates=trial_rates,residual=trial_residual)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']),flush=True)
                        fixed_q,fixed_p,velocity,evaluated,history = endpoint_inverse(evaluator,displaced,target,rates,
                            preconditioner,record)
                        evidence.check(probe_name+'_fixed_state_and_gravity', np.array_equal(fixed_q,displaced)
                            and np.array_equal(fixed_p,target) and evaluated['radial_residual'] < 2e-12
                            and evaluated['minimum_F'] > 0 and evaluated['maximum_speed_ratio'] < 1)
                        with localcontext() as context:
                            context.prec = 64
                            probe_residual = np.asarray(decimal_array(evaluated['momentum'])-target,float)
                        probe_correction = preconditioner.solve(probe_residual.ravel()).reshape(rates.shape)
                        sample = source_samples(owner,displaced,velocity,evaluated)
                        values = dict(coordinates=np.asarray(displaced,str),momenta=np.asarray(target,str),rates=velocity,
                            computed_momentum=evaluated['momentum'],preconditioned_residual=probe_correction,
                            radial_edges=evaluated['solver'].edges,radial_state=evaluated['solution']['state'],**sample)
                        path = evidence.output/(probe_name+'.npz')
                        np.savez_compressed(path,**values)
                        evidence.own(path,'outputs')
                        probes[index,sign] = values
                        evidence.report['probes'].append(dict(branch=branch,extension=extension,label=label,index=index,
                            sign=sign,step=step,path=str(path.relative_to(evidence.root)),iterations=len(history),
                            **{key:history[-1][key] for key in ['relative_residual','maximum_correction','radial_residual']},
                            valid_for_claim=False))
                        evidence.save()
                derivatives,richardson,physical,rows = analyze_probes(base,probes,steps)
                for row in rows:
                    evidence.report['derivative_checks'].append(dict(branch=branch,extension=extension,label=label,**row))
                analysis_path = evidence.output/(name+'-acceleration.npz')
                channels = {key:value for key,value in physical[-1].items()}
                channels.update({'richardson_'+str(index)+'_'+key:value for index,item in enumerate(richardson) for key,value in item.items()})
                channels.update({'direct'+str(index)+'_'+key:value for index,item in enumerate(derivatives) for key,value in item.items()})
                np.savez_compressed(analysis_path,**channels)
                evidence.own(analysis_path,'outputs')
                acceleration = richardson[-1]['acceleration']
                tangent_step = steps[-1]/2
                evaluated_tangents = {}
                for tangent_label,coordinate_direction,velocity_direction in [
                    ('coordinate',rates,np.zeros_like(rates)),('velocity',np.zeros_like(rates),acceleration),
                    ('joint',rates,acceleration)]:
                    for sign in [1,-1]:
                        displaced = advance_coordinates(position,coordinate_direction,sign*tangent_step,64)
                        velocity = rates+sign*tangent_step*velocity_direction
                        evaluated = evaluator.evaluate(displaced,velocity)
                        evidence.check(name+'-'+tangent_label+str(sign)+'_tangent_chart', evaluated['radial_residual'] < 2e-12
                            and evaluated['minimum_F'] > 0 and evaluated['maximum_speed_ratio'] < 1)
                        evaluated_tangents[tangent_label,sign] = evaluated['momentum']
                        path = evidence.output/(name+'-'+tangent_label+str(sign)+'-tangent.npz')
                        np.savez_compressed(path,coordinates=np.asarray(displaced,str),rates=velocity,momentum=evaluated['momentum'])
                        evidence.own(path,'outputs')
                        evidence.report['progress'] = dict(case=name+'-'+tangent_label+str(sign),seconds=perf_counter()-started)
                        evidence.save()
                tangent = {key:centered(evaluated_tangents[key,1],evaluated_tangents[key,-1],tangent_step)
                    for key in ['coordinate','velocity','joint']}
                force_float = np.asarray(force,float)
                scale = max(preconditioner.residual_norm(force_float),1e-30)
                for check_name,defect in [('full_chain_residual',tangent['coordinate']+tangent['velocity']-force_float),
                    ('joint_chain_residual',tangent['joint']-force_float),
                    ('split_versus_joint',tangent['coordinate']+tangent['velocity']-tangent['joint'])]:
                    error = preconditioner.residual_norm(defect)/scale
                    evidence.report['tangent_checks'].append(dict(branch=branch,extension=extension,label=label,
                        quantity=check_name,relative_residual=error,tolerance=2e-3,passed=bool(error < 2e-3),valid_for_claim=False))
                for sample_index in range(len(base['labels'])):
                    evidence.report['samples'].append(dict(branch=branch,extension=extension,label=label,
                        sample_index=sample_index,material_label=float(base['labels'][sample_index]),
                        kind='quadrature' if sample_index < 48 else ('node' if sample_index < 63 else 'center'),
                        radius=float(base['radius'][sample_index]),clock=float(base['clock'][sample_index]),
                        **{key:float(value[sample_index]) for key,value in physical[-1].items()},
                        source_path=str(analysis_path.relative_to(evidence.root)),valid_for_claim=False))
                evidence.save()
        evidence.check('complete_equal_branch_experiment',len(evidence.report['cases']) == 6
            and len(evidence.report['probes']) == 36 and len(evidence.report['samples']) == 384
            and len(evidence.report['derivative_checks']) == 30 and len(evidence.report['tangent_checks']) == 18)
        evidence.own(evidence.output/'latest-trial-recovery.npz','outputs')
        evidence.report.update(physical_acceleration_qualified=all(row['passed']
            for key in ['derivative_checks','tangent_checks'] for row in evidence.report[key]),
            evaluations=sum(1 for row in evidence.report['iterations'])+6+36,
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps({key:evidence.report[key] for key in ['state','physical_acceleration_qualified','seconds']}),flush=True)
    except Exception as error:
        recovery = evidence.output/'latest-trial-recovery.npz'
        if recovery.exists():
            evidence.own(recovery,'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
