from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_reaction_balance_20260921 import replay, sampled, label_balance, symbolic_balance
from annular_candidate_source_acceleration_20260921 import source_samples
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_candidate_hamiltonian_20260921 import decimals
from time import perf_counter
from pathlib import Path
import argparse
import contextlib
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds',type=float,default=7200)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-candidate-reaction-balance-attempt01',__file__)
    started = perf_counter()
    deadline = started+args.max_seconds
    try:
        helper = evidence.root/'scripts/annular_candidate_reaction_balance_20260921.py'
        evidence.own(helper)
        snapshot = evidence.output/('executed-'+helper.name)
        snapshot.write_bytes(helper.read_bytes())
        evidence.own(snapshot,'outputs')
        prior_path = evidence.output.parent/'annular-candidate-source-acceleration-v3-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        evidence.check('previous_acceleration_evidence_complete',prior['state'] == 'complete'
            and prior['physical_acceleration_qualified'] and prior['wider_endpoint_raw_reaction_qualified'])
        evidence.report.update(github_action=False,subagents_used=False,original_action_unchanged=True,
            full_components=16425,modes_deleted=False,replay_not_new_trajectory=True,
            reference_orders=[16,32],material_order=48,scientific_checks=[],summaries=[],replays=[],
            absolute_reaction_tolerance=1e-13,relative_reaction_tolerance=1e-3,
            inherited_failed_executions=prior['total_failed_attempts_preserved'],maximum_seconds=args.max_seconds)
        symbolic_balance(evidence)

        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key,prior['outputs'].get(key))
            evidence.check(path.name+'_sealed_input',expected is not None
                and hashlib.sha256(path.read_bytes()).hexdigest() == expected)
            evidence.own(path)
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as data:
                return {key:data[key].copy() for key in data.files}

        def progress(name):
            if perf_counter() > deadline:
                raise RuntimeError('Safe saved-work boundary reached during reaction decomposition.')
            evidence.report['progress'] = dict(stage=name,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)

        main_run = owned(evidence.output.parent/'annular-candidate-source-acceleration-attempt01/status.json')
        wide_run = owned(evidence.output.parent/'annular-candidate-source-acceleration-wide-probes-attempt01/status.json')
        points,weights = np.polynomial.legendre.leggauss(48)
        labels = points/2
        weights = weights/2*6*(labels+.5)*(.5-labels)
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257,branch == 'MTS',2e-5)
            saved = owned(evidence.output.parent/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(evidence.output.parent/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(evidence.output.parent/'annular-complete-frozen-candidate-attempt01'/(case+'-action.json'))
            owner,unused,unused_rates = common_material(native,saved,overlay)
            cardinal = np.polynomial.chebyshev.chebvander(2*labels,14) @ owner.layer_rule.inverse
            for label,run in [('initial',main_run),('endpoint-wide',wide_run)]:
                name = case+'-'+label
                progress(name+'-begin')
                case_row = next(row for row in run['cases'] if row['branch'] == branch
                    and row['extension'] == extension and row['label'] == label)
                base_saved = owned(evidence.root/case_row['path'])
                selected = [row for row in run['probes'] if row['branch'] == branch
                    and row['extension'] == extension and row['label'] == label]
                objects = {}
                state_rows = [dict(index=-1,sign=0,path=case_row['path'])]+selected
                for state_row in state_rows:
                    data = base_saved if state_row['index'] == -1 else owned(evidence.root/state_row['path'])
                    action,residual = replay(owner,overlay['overlay'],packet,extension,data,deadline)
                    sample = source_samples(owner,decimals(data['coordinates']),data['rates'],
                        dict(solver=action.solver,solution=action.solution))
                    sample_error = max(float(np.max(abs(sample[key]-data[key]))) for key in
                        ['mass','lapse','metric','clock','lapse_radial','metric_radial'])
                    evidence.check(name+'-replay-'+str(state_row['index'])+'-'+str(state_row['sign']),
                        residual < 2e-12 and sample_error < 2e-12,dict(radial_residual=residual,sample_error=sample_error))
                    objects[state_row['index'],state_row['sign']] = action
                    replay_path = evidence.output/(name+'-replay'+str(state_row['index'])+'-'+str(state_row['sign'])+'.npz')
                    np.savez_compressed(replay_path,edges=action.solver.edges,state=action.solution['state'],
                        rhs_coefficients=action.solution['rhs_coefficients'],primitives=action.solution['primitives'],left=action.solution['left'])
                    evidence.own(replay_path,'outputs')
                    evidence.report['replays'].append(dict(branch=branch,extension=extension,label=label,
                        index=state_row['index'],sign=state_row['sign'],source_path=state_row['path'],
                        replay_path=str(replay_path.relative_to(evidence.root)),radial_residual=residual,
                        sample_error=sample_error,valid_for_claim=False))
                    progress(name+'-replay-'+str(state_row['index'])+'-'+str(state_row['sign']))
                base = objects.pop((-1,0))
                evaluated = base.momentum_and_force(16,48,deadline)
                force = np.asarray(decimals(base_saved['force_decimal']),float)
                force_error = float(np.max(abs(evaluated['force']-force)))
                momentum_error = float(np.max(abs(evaluated['momentum']-base_saved['computed_momentum'])))
                evidence.check(name+'_original_action_force_momentum_replayed',force_error < 1e-12*max(np.max(abs(force)),1e-30)
                    and momentum_error < 1e-12*max(np.max(abs(base_saved['computed_momentum'])),1e-30),
                    dict(force_error=force_error,momentum_error=momentum_error))
                previous = [row for row in prior['dust_reaction_components'] if row['branch'] == branch
                    and row['extension'] == extension and row['label'] == label]
                previous.sort(key=lambda row:row['index'])
                raw_reaction = np.array([row['reaction'] for row in previous])
                root_rate = np.array([row['root_residual_derivative'] for row in previous])
                old_traction = owned(evidence.output.parent/('annular-candidate-source-acceleration-v3-'+name+'-traction.npz'))
                source_norm = max(float(np.linalg.norm(raw_reaction)),1e-30)
                tolerance = 1e-13+1e-3*source_norm
                orders = []
                for order in [16,32]:
                    rows,raw_rows = [],[]
                    for index,material_label in enumerate(labels):
                        channels,raw = label_balance(base,objects,run['derivative_steps'],material_label,order)
                        rows.append(channels)
                        raw_rows.append(raw)
                        if index % 8 == 7:
                            progress(name+'-order'+str(order)+'-labels'+str(index+1))
                    keys = list(rows[0])
                    table = np.array([[row[key] for key in keys] for row in rows])
                    projected = {key:cardinal.T @ (weights*table[:,index]) for index,key in enumerate(keys)}
                    decomposed = projected['anchor']+projected['internal']+projected['exterior']+projected['volume_1']+projected['gram']
                    lower_estimate = projected['anchor']+projected['internal']+projected['exterior']+projected['volume_0']+projected['gram']
                    direct_product = projected['direct_product_1']+projected['gram']
                    direct_difference = projected['direct_difference_1']+projected['gram']
                    boundary_sum = projected['anchor']+projected['internal']+projected['exterior']
                    science = dict(full_reaction_decomposition=np.linalg.norm(decomposed-raw_reaction),
                        integrated_cell_identity=np.linalg.norm(decomposed-direct_product),
                        source_momentum_product_rule=np.linalg.norm(direct_product-direct_difference),
                        matched_moving_quadrature=np.linalg.norm(direct_difference-raw_reaction),
                        derivative_estimate_change=np.linalg.norm(decomposed-lower_estimate))
                    for quantity,error in science.items():
                        evidence.report['scientific_checks'].append(dict(branch=branch,extension=extension,label=label,
                            order=order,quantity=quantity,error=float(error),tolerance=tolerance,passed=bool(error <= tolerance),valid_for_claim=False))
                    evidence.check(name+'-order'+str(order)+'_pointwise_identity',max(row['pointwise_identity_error_1'] for row in rows) < 1e-9,
                        max(row['pointwise_identity_error_1'] for row in rows))
                    evidence.check(name+'-order'+str(order)+'_same_Gram_force',np.max(abs(projected['gram']-evaluated['gram'][:,-1])) < 1e-14)
                    evidence.check(name+'-order'+str(order)+'_same_anchor_traction',
                        np.linalg.norm(projected['anchor']-old_traction['projected_traction']) < 1e-14)
                    offsets = np.r_[0,np.cumsum([len(row['reference']) for row in raw_rows])]
                    packed = {}
                    for key in raw_rows[0]:
                        if key in ['edge_left','edge_right','jump_density']:
                            packed[key] = np.stack([row[key] for row in raw_rows])
                        else:
                            packed[key] = np.concatenate([row[key] for row in raw_rows],axis=1 if key.startswith('probe_') else 0)
                    path = evidence.output/(name+'-order'+str(order)+'-balance.npz')
                    np.savez_compressed(path,labels=labels,weights=weights,cardinal=cardinal,offsets=offsets,
                        columns=np.asarray(keys),label_channels=table,derivative_steps=run['derivative_steps'],
                        raw_reaction=raw_reaction,root_residual_derivative=root_rate,
                        decomposed=decomposed,lower_estimate=lower_estimate,direct_product=direct_product,
                        direct_difference=direct_difference,force=force,bulk=evaluated['bulk'],dust=evaluated['dust'],gram=evaluated['gram'],
                        **{'projected_'+key:value for key,value in projected.items()},**packed)
                    evidence.own(path,'outputs')
                    summary = dict(branch=branch,extension=extension,label=label,order=order,
                        reaction_norm=source_norm,anchor_norm=float(np.linalg.norm(projected['anchor'])),
                        internal_jump_norm=float(np.linalg.norm(projected['internal'])),
                        cell_field_EL_norm=float(np.linalg.norm(projected['volume_1'])),
                        Gram_source_norm=float(np.linalg.norm(projected['gram'])),
                        boundary_only_remainder=float(np.linalg.norm(raw_reaction-projected['anchor'])),
                        full_remainder=float(np.linalg.norm(raw_reaction-decomposed)),
                        full_remainder_relative_to_reaction=float(np.linalg.norm(raw_reaction-decomposed)/source_norm),
                        interior_cancellation=float((np.linalg.norm(projected['internal'])+np.linalg.norm(projected['volume_1'])
                            +np.linalg.norm(projected['gram']))/max(np.linalg.norm(projected['internal']+projected['volume_1']+projected['gram']),1e-30)),
                        boundary_quadrature_defect=float(np.linalg.norm(projected['boundary_integral']-boundary_sum)),
                        source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                    evidence.report['summaries'].append(summary)
                    orders.append(decomposed)
                    evidence.save()
                    print(json.dumps(summary),flush=True)
                    del raw_rows,packed
                error = float(np.linalg.norm(orders[1]-orders[0]))
                evidence.report['scientific_checks'].append(dict(branch=branch,extension=extension,label=label,
                    order=32,quantity='reference_quadrature_16_32',error=error,tolerance=tolerance,passed=error <= tolerance,valid_for_claim=False))
                evidence.report['cases'].append(dict(branch=branch,extension=extension,label=label,
                    source_path=case_row['path'],reference_orders=[16,32],valid_for_claim=False))
                progress(name+'-complete')
        evidence.check('equal_branch_full_experiment',len(evidence.report['cases']) == 6
            and len(evidence.report['replays']) == 42 and len(evidence.report['summaries']) == 12
            and len(evidence.report['scientific_checks']) == 66)
        evidence.report.update(seconds=perf_counter()-started,reaction_decomposition_qualified=all(row['passed'] for row in evidence.report['scientific_checks']))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state=evidence.report['state'],qualified=evidence.report['reaction_decomposition_qualified'],seconds=evidence.report['seconds'])),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
