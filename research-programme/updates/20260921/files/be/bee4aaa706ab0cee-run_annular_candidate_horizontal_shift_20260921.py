from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_horizontal_shift_20260921 import CachedTangent,current_comparison,shift_spot
from annular_candidate_energy_current_20260921 import build_base
from annular_candidate_Ward_source_20260921 import probe_action
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
    evidence = EvidenceRun('annular-candidate-horizontal-shift-attempt01',__file__)
    started,deadline = perf_counter(),perf_counter()+args.max_seconds
    try:
        for name in ['scripts/annular_candidate_horizontal_shift_20260921.py',
            'DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md',
            'DERIVATION-20260918-moving-P2-current-and-live-evolution.md',
            'scripts/qualify_annular_P2_shift_variation_20260918.py']:
            path = evidence.root/name
            evidence.own(path)
        prior_path = evidence.output.parent/'annular-moving-Legendre-current-final-integrity.json'
        evidence.own(prior_path)
        prior = json.loads(prior_path.read_text())
        evidence.check('prior_localized_current_complete',prior['state']=='complete')
        evidence.report.update(scientific_checks=[],summaries=[],shift_spots=[],full_components=16425,
            original_diagonal_action_unchanged=True,new_trajectory=False,github_action=False,subagents_used=False,
            inherited_horizontal_extension=True,unique_parent_extension_proven=False,
            phase='endpoint-wide',orders=[8,12],energy_tolerance=2e-11,
            acceleration_modes=['action-coarse-tangent','action-fine-tangent','archived-coarse-tangent','archived-fine-tangent'],
            inherited_failed_executions=prior['total_failed_attempts_preserved'])
        def owned(path):
            key = str(path.relative_to(evidence.root))
            expected = prior['inputs'].get(key,prior['outputs'].get(key))
            evidence.check(path.name+'_sealed',expected is not None and hashlib.sha256(path.read_bytes()).hexdigest()==expected)
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
                raise RuntimeError('Safe saved-work boundary reached.')
        def scientific(case,name,value,tolerance):
            evidence.report['scientific_checks'].append(dict(case=case,quantity=name,error=float(value),
                tolerance=float(tolerance),passed=bool(np.isfinite(value) and value<=tolerance),valid_for_claim=False))
        replays = owned(evidence.output.parent/'annular-candidate-reaction-balance-attempt02/status.json')['replays']
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
            loads,action = build_base(owner,overlay['overlay'],packet,extension,states[-1,0],archives[-1,0],deadline)
            probes = {key:probe_action(action,states[key],archives[key]) for key in states if key!=(-1,0)}
            system = owned(evidence.output.parent/'annular-moving-Legendre-current-attempt01'/(name+'-system.npz'))
            tangent = CachedTangent(probes,system['steps'])
            accelerations = np.concatenate([system['acceleration'],system['archived_acceleration']])
            evidence.check(name+'_all_components',accelerations.shape==(4,15,1095))
            for label in [-.31,0.,.27]:
                for profile in [0,1,2]:
                    spot = shift_spot(action,loads,tangent,states[-1,0],system['archived_acceleration'][-1],label,profile)
                    filename = name+'-label'+str(label)+'-profile'+str(profile)+'-shift.npz'
                    path = evidence.output/filename
                    np.savez_compressed(path,**spot)
                    evidence.own(path,'outputs')
                    evidence.check(filename+'_zero_shift_baseline',np.max(abs(spot['zero']-spot['baseline']))<2e-13)
                    for index,sector in enumerate(['wave','Gram','dust']):
                        absolute = 2e-18 if sector=='Gram' else 2e-12
                        scientific(filename,sector+'_finite_shift_derivative',spot['error'][index],absolute+2e-7*abs(spot['raw'][index]))
                    evidence.report['shift_spots'].append(dict(branch=branch,extension=extension,label=label,profile=profile,
                        wave_error=float(spot['error'][0]),Gram_error=float(spot['error'][1]),dust_error=float(spot['error'][2]),
                        omitted_moving_clock=float(spot['omitted_moving_clock']),source_path=str(path.relative_to(evidence.root)),valid_for_claim=False))
                    progress(filename+'-complete')
            currents = []
            for order in [8,12]:
                previous = owned(evidence.output.parent/'annular-moving-Legendre-current-attempt01'/(name+'-order'+str(order)+'-localized.npz'))
                ward = owned(evidence.output.parent/'annular-candidate-Ward-source-attempt01'/(name+'-order'+str(order)+'-Ward.npz'))
                result = current_comparison(action,loads,tangent,previous['targets'],accelerations,previous,ward,order,
                    deadline,lambda stage:progress(name+'-'+stage))
                identity_error = float(np.max(abs(result['current']-result['expected'])))
                current_difference = result['current']-previous['current'][[0,1,0,1]]
                noether = float(np.max(abs(result['label_whole_layer_Noether'])))
                case = name+'-order'+str(order)
                scientific(case,'independent_shift_Legendre_projection_identity',identity_error,2e-11)
                scientific(case,'whole_layer_Noether_identity',noether,2e-11)
                scientific(case,'archived_horizontal_equals_Legendre',np.max(abs(current_difference[2:])),2e-11)
                scientific(case,'action_horizontal_equals_Legendre',np.max(abs(current_difference[:2])),2e-11)
                mass_residual = previous['old_mass_residual']+previous['conversion']*(result['current'][3,1:-1]-previous['old_energy_current'])
                predicted_gap = np.concatenate([-result['sum_localized_Euler_work'][:2],
                    previous['projection']-result['sum_localized_Euler_work'][2:]])
                evidence.check(case+'_finite',all(np.all(np.isfinite(value)) for value in result.values()))
                path = evidence.output/(case+'-current.npz')
                np.savez_compressed(path,**result,legendre=previous['current'],difference=current_difference,predicted_gap=predicted_gap,
                    mass_residual=mass_residual,old_mass_residual=previous['old_mass_residual'],
                    legendre_mass_residual=previous['corrected_mass'],conversion=previous['conversion'],
                    gram_advection=previous['gram_advection'])
                evidence.own(path,'outputs')
                summary = dict(branch=branch,extension=extension,order=order,labels=len(result['labels']),
                    identity_error=identity_error,whole_layer_Noether_error=noether,
                    archived_current_difference_max=float(np.max(abs(current_difference[2:]))),
                    action_current_difference_max=float(np.max(abs(current_difference[:2]))),
                    archived_cut_residual_work_max=float(np.max(abs(result['sum_localized_Euler_work'][2:]))),
                    action_cut_residual_work_max=float(np.max(abs(result['sum_localized_Euler_work'][:2]))),
                    mass_residual_max=float(np.max(abs(mass_residual))),source_path=str(path.relative_to(evidence.root)),valid_for_claim=False)
                evidence.report['summaries'].append(summary)
                evidence.report['cases'].append(summary)
                currents.append(result['current'])
                progress(case+'-complete')
                print(json.dumps(summary),flush=True)
            scientific(name,'paired_quadrature_8_12',np.max(abs(currents[1]-currents[0])),2e-11)
        evidence.report.update(seconds=perf_counter()-started,
            comparisons_passed=all(row['passed'] for row in evidence.report['scientific_checks']))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',seconds=evidence.report['seconds'],comparisons_passed=evidence.report['comparisons_passed'])),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
