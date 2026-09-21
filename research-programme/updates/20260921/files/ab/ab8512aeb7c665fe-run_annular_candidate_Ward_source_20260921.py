from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_Ward_source_20260921 import symbolic_controls,probe_action,material_quadrature,label_source
from annular_candidate_energy_current_20260921 import build_base
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from time import perf_counter
import argparse
import contextlib
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seconds',type=float,default=10500)
    args = parser.parse_args()
    evidence = EvidenceRun('annular-candidate-Ward-source-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        helper = evidence.root/'scripts/annular_candidate_Ward_source_20260921.py'
        evidence.own(helper)
        snapshot = evidence.output/('executed-'+helper.name)
        snapshot.write_bytes(helper.read_bytes())
        evidence.own(snapshot,'outputs')
        prior_path = evidence.output.parent/'annular-candidate-energy-current-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        evidence.check('prior_current_evidence_complete',prior['state']=='complete')
        evidence.report.update(scientific_checks=[],summaries=[],source_components=[],full_components=16425,
            original_action_unchanged=True,new_trajectory=False,github_action=False,subagents_used=False,
            phase='endpoint-wide',reference_and_material_orders=[8,12],prediction_absolute_tolerance=5e-12,
            prediction_relative_tolerance=.05,quadrature_tolerance=1e-12,
            inner_current_assumption='Constant central mass and no incoming wave/Gram current below all supports.',
            inherited_failed_executions=prior['total_failed_attempts_preserved'])
        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key,prior['outputs'].get(key))
            evidence.check(path.name+'_sealed_input',expected is not None and hashlib.sha256(path.read_bytes()).hexdigest()==expected)
            evidence.own(path)
            if path.suffix=='.json':
                return json.loads(path.read_text())
            with np.load(path,allow_pickle=False) as archive:
                return {key:archive[key].copy() for key in archive.files}
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage,seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']),flush=True)
            if perf_counter()>deadline:
                raise RuntimeError('Saved label boundary reached at wall limit.')
        symbolic_controls(evidence)
        replays = owned(evidence.output.parent/'annular-candidate-reaction-balance-attempt02/status.json')['replays']
        reference = owned(evidence.output.parent/'annular-candidate-energy-current-attempt01/reference-reference-endpoint-wide-currents.npz')
        radius = reference['radius']
        base_reference = next(row for row in replays if row['extension']=='reference' and row['label']=='endpoint-wide' and row['index']==-1)
        reference_state = owned(evidence.root/base_reference['source_path'])
        source_radius = float(np.mean(np.asarray(reference_state['coordinates'][:,-1],float)))
        indices = [0,len(radius)-1,int(np.argmax(abs(reference['bare_residual'])))]
        for mask in [(radius<source_radius)&(reference['wave48_source_density']==0),
            (radius>source_radius)&(reference['wave48_source_density']==0)]:
            selected = np.flatnonzero(mask)
            indices.append(int(selected[np.argmax(abs(reference['wave48_wave_mass_current'][selected]))]))
        indices = np.unique(indices)
        targets = radius[indices]
        evidence.report.update(target_grid_indices=indices.tolist(),target_radii=targets.tolist(),
            target_selection='Prior reference grid: extremes, maximum defect, and maximum wave current on either side of source; diagnostic, not held-out.')
        for branch,extension in [('reference','reference'),('MTS','primary'),('MTS','alternative')]:
            name = branch+'-'+extension
            progress(name+'-begin')
            native = IndexedGradedP2System(257,branch=='MTS',2e-5)
            original = owned(evidence.output.parent/'annular-candidate-initial-metric-attempt02'/(branch+'-velocity-owned-inputs.npz'))
            overlay = owned(evidence.output.parent/'annular-transfer-kernel-overlay-attempt01'/(branch+'-exact-common-overlay.json'))
            packet = owned(evidence.output.parent/'annular-complete-frozen-candidate-attempt01'/(name+'-action.json'))
            owner,unused,unused_rates = common_material(native,original,overlay)
            selected = [row for row in replays if row['branch']==branch and row['extension']==extension and row['label']=='endpoint-wide']
            states = {(row['index'],row['sign']):owned(evidence.root/row['source_path']) for row in selected}
            archives = {(row['index'],row['sign']):owned(evidence.root/row['replay_path']) for row in selected}
            loads,base = build_base(owner,overlay['overlay'],packet,extension,states[-1,0],archives[-1,0],deadline)
            probes = {key:probe_action(base,states[key],archives[key]) for key in states if key!=(-1,0)}
            old_current = owned(evidence.output.parent/'annular-candidate-energy-current-attempt01'/(name+'-endpoint-wide-currents.npz'))
            evidence.check(name+'_same_physical_grid',np.array_equal(old_current['radius'],radius))
            evidence.check(name+'_cuts_avoid_source_support',np.all(old_current['wave48_source_density'][indices]==0))
            observed = old_current['conditional_residual'][indices]
            conversion = old_current['wave48_conversion'][indices]
            tolerance = 5e-12+.05*max(float(np.max(abs(observed))),1e-30)
            predictions = []
            for order in [8,12]:
                labels,weights,cuts = material_quadrature(loads,targets,order)
                rows = []
                spot_index = int(np.argmin(abs(labels)))
                for index,label in enumerate(labels):
                    row,spot = label_source(base,loads,probes,old_current['steps'],targets,label,order)
                    rows.append(row)
                    if index==spot_index:
                        path = evidence.output/(name+'-order'+str(order)+'-spot.npz')
                        np.savez_compressed(path,**spot,label=label,targets=targets,steps=old_current['steps'])
                        evidence.own(path,'outputs')
                    if index%8==7 or index==len(labels)-1:
                        progress(name+'-order'+str(order)+'-labels'+str(index+1)+'of'+str(len(labels)))
                channels = {key:np.stack([row[key] for row in rows]) for key in rows[0]}
                summed = {key:np.tensordot(weights,channels[key],axes=(0,0)) for key in
                    ['volume','internal','anchor','exterior','dust','gram_field','gram_source','total']}
                predicted = -conversion*summed['total']
                error = float(np.max(abs(predicted[-1]-observed)))
                sensitivity = float(np.max(abs(predicted[-1]-predicted[0])))
                evidence.check(name+'-order'+str(order)+'_finite_and_positive_measure',
                    np.all(np.isfinite(predicted)) and min(weights)>0 and abs(sum(weights)-1)<1e-12)
                evidence.check(name+'-order'+str(order)+'_face_trace_identity',
                    np.max(abs(channels['face_power']-channels['face_average']*channels['face_EL']))<1e-16)
                for quantity,value in [('independent_Ward_prediction',error),('source_derivative_estimate_change',sensitivity)]:
                    evidence.report['scientific_checks'].append(dict(branch=branch,extension=extension,order=order,
                        quantity=quantity,error=value,tolerance=tolerance,passed=bool(value<=tolerance),valid_for_claim=False))
                path = evidence.output/(name+'-order'+str(order)+'-Ward.npz')
                np.savez_compressed(path,labels=labels,weights=weights,cuts=cuts,targets=targets,steps=old_current['steps'],
                    observed=observed,conversion=conversion,predicted=predicted,spot_index=spot_index,
                    **{'label_'+key:value for key,value in channels.items()},**{'sum_'+key:value for key,value in summed.items()})
                evidence.own(path,'outputs')
                summary = dict(branch=branch,extension=extension,order=order,labels=len(labels),targets=len(targets),
                    observed_max=float(np.max(abs(observed))),prediction_max=float(np.max(abs(predicted[-1]))),
                    prediction_error=error,prediction_derivative_sensitivity=sensitivity,
                    source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                evidence.report['summaries'].append(summary)
                for index,target in enumerate(targets):
                    evidence.report['source_components'].append(dict(branch=branch,extension=extension,order=order,radius=float(target),
                        observed=float(observed[index]),predicted=float(predicted[-1,index]),
                        **{key:float(-conversion[index]*(value[-1,index] if value.ndim==2 else value[index]))
                            for key,value in summed.items() if key!='total'},valid_for_claim=False))
                predictions.append(predicted[-1])
                evidence.report['cases'].append(summary)
                progress(name+'-order'+str(order)+'-complete')
                print(json.dumps(summary),flush=True)
            difference = float(np.max(abs(predictions[1]-predictions[0])))
            evidence.report['scientific_checks'].append(dict(branch=branch,extension=extension,order=12,
                quantity='paired_quadrature_8_12',error=difference,tolerance=1e-12,passed=difference<=1e-12,valid_for_claim=False))
        evidence.check('matched_endpoint_experiment_complete',len(evidence.report['cases'])==6 and len(evidence.report['scientific_checks'])==15)
        evidence.report.update(seconds=perf_counter()-started,prediction_qualified=all(row['passed'] for row in evidence.report['scientific_checks']))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],qualified=evidence.report['prediction_qualified'])),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
